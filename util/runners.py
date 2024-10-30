from typing import Any
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
from datetime import datetime
from huggingface_hub import hf_hub_download
from transformers import VideoLlavaProcessor, VideoLlavaForConditionalGeneration, BitsAndBytesConfig
from PIL import Image
import numpy as np
import av
import torch
import os
from llama_cpp import Llama
from dotenv import load_dotenv
import os
from diffusers import AutoPipelineForText2Image, DiffusionPipeline, FluxPipeline
import torch
import os
import numpy as np
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.distributed as dist
import torch.optim
import torch.multiprocessing as mp
import torch.utils.data
import torch.utils.data.distributed
from bart import BartCaptionModel
from utils.eval_utils import load_pretrained
from utils.audio_utils import load_audio, STR_CH_FIRST

from mistralrs import Runner, Which, ChatCompletionRequest, VisionArchitecture
from ragatouille import RAGPretrainedModel


import sys 


sys.path.append('../util')



load_dotenv()



class MusicRunner:

    def __init__(self) -> None:

        model, save_epoch = load_pretrained('music-caps', gpu_id=0, max_length=128, num_beams=5, model_type='last' )
        torch.cuda.set_device(0)
        self.model = model.cuda(0)


    def __call__(self, audio_path) -> Any:

        def get_audio(audio_path, duration=10, target_sr=16000):

            n_samples = int(duration * target_sr)
            audio, sr = load_audio(
                path= audio_path,
                ch_format= STR_CH_FIRST,
                sample_rate= target_sr,
                downmix_to_mono= True,
            )
            if len(audio.shape) == 2:
                audio = audio.mean(0, False)  # to mono
            input_size = int(n_samples)
            if audio.shape[-1] < input_size:  # pad sequence
                pad = np.zeros(input_size)
                pad[: audio.shape[-1]] = audio
                audio = pad
            ceil = int(audio.shape[-1] // n_samples)
            audio = torch.from_numpy(np.stack(np.split(audio[:ceil * n_samples], ceil)).astype('float32'))
            return audio
            
        self.model.eval()

        audio_tensor = get_audio(audio_path)
        audio_tensor = audio_tensor.cuda(0, non_blocking=True)

        with torch.no_grad():
            output = self.model.generate(
                samples=audio_tensor,
                num_beams=5,
            )

        inference = {}

        res = ""

        number_of_chunks = range(audio_tensor.shape[0])
        for chunk, text in zip(number_of_chunks, output):

            time = f"{chunk * 10}:00-{(chunk + 1) * 10}:00"
            item = {"text":text,"time":time}
            inference[chunk] = item

            res += text

        return res




class TextRunner:


    def __init__(self, ctx_size, **kwargs) -> None:
        """
        Initializes an instance of the class with the given parameters.

        Parameters:
            local (bool): Indicates whether the instance is local or not.
            ctx_size (int): The size of the context.

        Returns:
            None

        Initializes the instance with the given parameters. If `local` is True, an instance of the Llama class is created with the specified model path, chat format, GPU layers, context size, and temperature. Otherwise, the `llm` attribute is set to None.

        Note: The model path is specific to the current codebase and may need to be updated accordingly.
        """


        pesimistic = kwargs.get("pesimistic", False)
        quality = kwargs.get("quality", "medium")

        if pesimistic:
            
            self.llm = Llama(
                model_path="L3-Dark-Planet-8B-D_AU-Q4_k_m.gguf",
                chat_format="llama-3",
                n_gpu_layers=-1,
                n_ctx=ctx_size,
                temperature=0.2
            )

            

        else:


            if quality == "medium":

                self.llm = Llama(
                    model_path="Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
                    chat_format="llama-3",
                    n_gpu_layers=-1,
                    n_ctx=ctx_size,
                    temperature=0.2
                )

            elif quality == "high":

                self.llm = Llama(
                    model_path="Meta-Llama-3.1-8B-Instruct-Q6_K_L.gguf",
                    chat_format="llama-3",
                    n_gpu_layers=-1,
                    n_ctx=ctx_size,
                    temperature=0.2
                )
        
            else:

                self.llm = Llama(
                    model_path="Meta-Llama-3.1-8B-Instruct-IQ2_M.gguf",
                    chat_format="llama-3",
                    n_gpu_layers=-1,
                    n_ctx=ctx_size,
                    temperature=0.2
                )
        






    
    def __call__(self, template, prompt) -> Any:
        """
        Executes the command runner with the given template, prompt, and tools.

        Args:
            template (str): The template for the command runner.
            prompt (str): The prompt for the command runner.

        Returns:
            Any: The output of the command runner.

        If the command runner is local, it executes the Llama model with the given template, tools, and prompt, 
        using the specified system prompt template and maximum context size. The output is generated using the 
        specified stop tokens and echoing is enabled.

        If the command runner is not local, it concatenates the template and prompt, and calls the chat method of 
        the Llama model with the role set to the template and the message set to the concatenated prompt and model 
        set to 'command-r'.
        """

        output = self.llm.create_chat_completion(
            messages = [
                    {"role": "system", "content": template},
                    {
                        "role": "user",
                        "content": prompt 
                    }
                ]
        )
        
      



class RAG:


    def __init__(self) -> None:
        

        self.RAG = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")

        # Initialize the graph database with Graphiti's indices. This only needs to be done once.


    def __call__(self, collection,documents) -> None:
        """
        Executes a query on the collection based on the given document and returns the results.

        Args:
            collection (str): The name of the collection to query.
            k_value (int): The number of results to return.
            hallucinate (bool): Whether to hallucinate results or not.
            document (str): The document to query.

        Returns:
            None: If hallucinate is True and k_value is greater than the number of results.
            list: A list of the top k_value results. If hallucinate is False, the list contains the top k_value results. If hallucinate is True, the list contains the top k_value results from the hallucinated results.
        """

        self.memory = RAG.index(index_name=collection, collection=documents)
         
    
    
    def aggregate(self, query, k, hallucinate) -> str:
        
        """

        Queries the graph database with the given query string and returns the results as a list of strings.
        
        Parameters
        ----------
        query : str
            A string representing the Cypher query to execute.
        
        Returns
        -------
        list
            A list of strings representing the results of the query.
        """
        results =  self.memory.search(query, k=k)

        if hallucinate:

            results = [doc.content for doc in results]
        
        #reverses the restults

        else:

            results = [doc.content for doc in reversed(results)]

        return results



class VideoLlavaRunner:


    def __init__(self) -> None:


        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
        )

        self.model = VideoLlavaForConditionalGeneration.from_pretrained("video-llava/Video-LLaVA-7B",torch_dtype=torch.float16, quantization_config=quantization_config)
        self.processor = VideoLlavaProcessor.from_pretrained("video-llava/Proc-Video-LLaVA-7B")



    def __call__(self, video_path) -> Any:
        
        def read_video_pyav(container, indices):
            '''
            Decode the video with PyAV decoder.

            Args:
                container (av.container.input.InputContainer): PyAV container.
                indices (List[int]): List of frame indices to decode.

            Returns:
                np.ndarray: np array of decoded frames of shape (num_frames, height, width, 3).
            '''
            frames = []
            container.seek(0)
            start_index = indices[0]
            end_index = indices[-1]
            for i, frame in enumerate(container.decode(video=0)):
                if i > end_index:
                    break
                if i >= start_index and i in indices:
                    frames.append(frame)
            return np.stack([x.to_ndarray(format="rgb24") for x in frames])

        prompt = "USER: <video>Descibe in great detail the visual ambiance and overtone of the scene. Do a symobolic analysis of the scene aswell ASSISTANT:"
        video_path = 'test.mp4' 
        container = av.open(video_path)

        # sample uniformly 8 frames from the video
        total_frames = container.streams.video[0].frames

        cumm_sum = 0

        res = ""

        for i in range(total_frames):

            if cumm_sum == 8:

                print(i - 8 )
                indices = np.arange(i - 8 , total_frames, total_frames/8).astype(int)
                clip = read_video_pyav(container, indices)

                inputs = self.processor(text=prompt, videos=clip, return_tensors="pt")

                # Generate
                generate_ids = self.model.generate(**inputs, max_length=2048)

                inference = self.processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
                print(inference)

                res += inference

                cumm_sum = 0
            else:
                cumm_sum += 1   

        return res
             

class FluxRunner:




    def __init__(self) -> None:
        """
        Initializes an instance of the class with the given parameters.

        Returns:
            None

        Initializes the instance with the given parameters. If `local` is True, an instance of the AutoPipelineForText2Image class is created with the specified model path, torch data type, and variant. If `low_power` is False, the model is moved to the CUDA device.
        """

        self.model  = FluxPipeline.from_pretrained("flux", torch_dtype=torch.bfloat16)

        self.model.vae.enable_tiling()
        self.model.vae.enable_slicing()
        self.model.enable_sequential_cpu_offload() # offloads modules to CPU on a submodule level (rather than model level)

            



    def __call__(self, prompt) -> Any:
        """
        Executes the function with the given prompt.

        Args:
            prompt (str): The prompt for generating the image.

        Returns:
            Any: The generated image.

        If the function is executed locally, it uses the `model` attribute to generate the image with the given prompt.
        The generated image is obtained from the first element of the `images` list returned by the `model` method.

        If the function is not executed locally, it uses the `replicate.run` method to run the "stability-ai/sdxl:7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc" model.
        The input to the model includes the prompt, various parameters for image generation, such as width, height, refine, scheduler, num_outputs, guidance_scale, high_noise_frac, prompt_strength, and num_inference_steps.

        The generated image is returned.
        """


        image = self.model(
            prompt=prompt,
            guidance_scale=0.,
            height=768,
            width=1360,
            num_inference_steps=4,
            max_sequence_length=256,
        ).images[0]


        return image


        



class SDXLRunner:




    def __init__(self) -> None:
        """
        Initializes an instance of the class with the given parameters.

          Returns:
            None

        Initializes the instance with the given parameters. If `local` is True, an instance of the AutoPipelineForText2Image class is created with the specified model path, torch data type, and variant. If `low_power` is False, the model is moved to the CUDA device.
        """
     


        self.model = DiffusionPipeline.from_pretrained("sdxl-base", torch_dtype=torch.float16, use_safetensors=True, variant="fp16", device_map="balanced")
            



    def __call__(self, prompt) -> Any:
        """
        Executes the function with the given prompt.

        Args:
            prompt (str): The prompt for generating the image.

        Returns:
            Any: The generated image.

        If the function is executed locally, it uses the `model` attribute to generate the image with the given prompt.
        The generated image is obtained from the first element of the `images` list returned by the `model` method.

        If the function is not executed locally, it uses the `replicate.run` method to run the "stability-ai/sdxl:7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc" model.
        The input to the model includes the prompt, various parameters for image generation, such as width, height, refine, scheduler, num_outputs, guidance_scale, high_noise_frac, prompt_strength, and num_inference_steps.

        The generated image is returned.
        """


        image = self.model(prompt=prompt, num_inference_steps=10).images[0]

        return image


class ImageRunner:



    def __init__(self, low_power) -> None:
        """
        Initializes an instance of the class with the given parameters.

        Parameters:
            local (bool): Indicates whether the instance is local or not.
            low_power (bool): Indicates whether to use low power mode or not.

        Returns:
            None

        Initializes the instance with the given parameters. If `local` is True, an instance of the AutoPipelineForText2Image class is created with the specified model path, torch data type, and variant. If `low_power` is False, the model is moved to the CUDA device.
        """

        self.model =  AutoPipelineForText2Image.from_pretrained("models/sdxl-turbo", torch_dtype=torch.float16, variant="fp16")
            
        if not low_power: self.model.to("cuda")



    def __call__(self, prompt) -> Any:
        """
        Executes the function with the given prompt.

        Args:
            prompt (str): The prompt for generating the image.

        Returns:
            Any: The generated image.

        If the function is executed locally, it uses the `model` attribute to generate the image with the given prompt.
        The generated image is obtained from the first element of the `images` list returned by the `model` method.

        If the function is not executed locally, it uses the `replicate.run` method to run the "stability-ai/sdxl:7762fd07cf82c948538e41f63f77d685e02b063e37e496e96eefd46c929f9bdc" model.
        The input to the model includes the prompt, various parameters for image generation, such as width, height, refine, scheduler, num_outputs, guidance_scale, high_noise_frac, prompt_strength, and num_inference_steps.

        The generated image is returned.
        """


        image = self.model(prompt=prompt, num_inference_steps=1, guidance_scale=0.0).images[0]

        return image

from llama_cpp.llama_chat_format import Llava15ChatHandler

class LlavaRunner:



    def __init__(self, power='low') -> None:
        """
        Initializes an instance of the class with the given parameters.

            Returns:
            None

        Initializes the instance with the given parameters. If `local` is True, an instance of the Llama class is created with the specified model path, chat handler, context size, and logits all flag. The model path and chat handler are specific to the current codebase and may need to be updated accordingly.

        The `local` attribute is set to the value of the `local` parameter.

        If `local` is True, an instance of the Llama class is created with the following parameters:
            - model_path: The path to the Llama model file.
            - chat_handler: The chat handler for the Llama model.
            - n_ctx: The context size.
            - logits_all: The flag indicating whether to generate logits for all tokens.
        """

        self.power = power

        if power == 'high' :

            self.llm = Runner(
                which=Which.VisionPlain(
                    model_id="Llama-3.2-11B-Vision-Instruct-UQFF",
                    arch=VisionArchitecture.VLlama,
                ),
            )
        else:
            chat_handler = Llava15ChatHandler(clip_model_path="../models/mmproj.bin")
            llm = Llama(
                model_path="../models/ggml-model-q5_k.gguf",
                chat_handler=chat_handler,
                n_ctx=2048, 
            )

        

    def __call__(self, ctx_size, prompt, image_path) -> Any:
        """
        Executes the command runner with the given template, prompt, and image path.

        Args:
            template (str): The template for the command runner.
            prompt (str): The prompt for the command runner.
            image_path (str): The path to the image file.

        Returns:
            Any: The output of the command runner.

        If the command runner is local, it executes the Llama model with the given template, prompt, and image path.
        The output is generated using the specified system prompt template and maximum context size.
        The image is passed as a part of the chat completion.

        If the command runner is not local, it executes the Llama model with the given template, prompt, and image path.
        The output is generated using the specified parameters for the replicate.run method.
        The image is passed as a part of the input.

        The output of the command runner is returned.
        """

        if self.power == 'high':
  
        
            res = self.llm.send_chat_completion_request(
            ChatCompletionRequest(
                model="llama-vision",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": "file:///" + image_path
                                },
                            },
                            {
                                "type": "text",
                                "text": prompt,
                            },
                        ],
                    }
                ],
                max_tokens=ctx_size,
                presence_penalty=1.0,
                top_p=0.1,
                temperature=0.1,
                )
            )

            return res

        else:

            self.llm.create_chat_completion(
                messages = [
                    {"role": "system", "content": "You are an assistant who perfectly describes images."},
                    {
                        "role": "user",
                        "content": [
                            {"type" : "text", "text": "What's in this image?"},
                            {"type": "image_url", "image_url": {"url": "C://Users//def78//smenos//reaper//reaper//models//test.png" } }
                        ]
                    }
                ]
                )

