

def _map_doc_to_coefficient(doc):


    if len(doc) < 512:


        return 1
    

    elif len(doc) < 1024:


        return 2


    elif len(doc) < 2048:


        return 3





def map_document_size_to_n_summary_paragraphs(runner, coefficient):


    if runner == 'PHI_MINI'  or runner == 'LLAMA_70B' or runner == 'LLAMA_8B':


        if coefficient == 12:

            return 3200
        
        elif coefficient == 11:

            return 2500

        elif coefficient == 10:

            return 2000

        elif coefficient == 9:

            return 1800

        elif coefficient == 8:

            return 1600

        elif coefficient == 7:

            return 1300

        elif coefficient == 6:

            return 1000  

        elif coefficient == 5:

            return 800

        elif coefficient == 4:

            return 600

        elif coefficient == 3:

            return 400

        elif coefficient == 2:

            return 300

        elif coefficient == 1:

            return 200

       
        else:

            raise ValueError('Coefficient must be between 1 and 12')


           
def map_coefficient_to_ctx_size(coefficient):

    if coefficient == 1:

        return 120

    elif coefficient == 2:

        return 240

    elif coefficient == 3:

        return 350

    elif coefficient == 4:

        return 460

    elif coefficient == 5:

        return 512
    
    elif coefficient == 6:

        return 1024

    elif coefficient == 7:

        return 2048

    elif coefficient == 8:

        return 3096

    elif coefficient == 9:

        return 4096
    
    elif coefficient == 10:

        return 6144
    
    elif coefficient == 11:

        return 7192
    
    elif coefficient == 12:

        return 8192 


    elif coefficient == 13:

        return 9216
    
    elif coefficient == 14:

        return 10240
    
    elif coefficient == 15:

        return 12288
    
    elif coefficient == 16:

        return 16384
    
    elif coefficient == 17:

        return 20480
    
    elif coefficient == 18:

        return 24576
    
    elif coefficient == 19:

        return 28672
    
    elif coefficient == 20:

        return 32768
    
    elif coefficient == 21:

        return 36864
    
    elif coefficient == 22:

        return 40960
    
    elif coefficient == 23:

        return 49152
    
    elif coefficient == 24:

        return 57344
    
    elif coefficient == 25:

        return 65536
    
    elif coefficient == 26:

        return 73728
    
    elif coefficient == 27:

        return 81920
    
    elif coefficient == 28:

        return 90112
    
    elif coefficient == 29:

        return 98304
    
    elif coefficient == 30:

        return 1048576

    elif coefficient == 31:

        return 1228800

    elif coefficient == 32:

        return 122333

    elif coefficient == 33:

        return 130000

    else:

        raise ValueError('Energy for llama must be between 1 and 12')


def _map_coefficient_to_rag_k(coefficient):


    if coefficient == 1:

        return 1

    elif coefficient == 2:

        return 4

    elif coefficient == 3:

        return 8

    elif coefficient == 4:

        return 12

    elif coefficient == 5:

        return 16

    elif coefficient == 6:

        return 20

    elif coefficient == 7:

        return 24
    
    elif coefficient == 8:

        return 30
    
    elif coefficient == 9:

        return 40
    
    elif coefficient == 10:

        return 60
    
    elif coefficient == 11:

        return 70
    
    elif coefficient == 12:

        return 80


    elif coefficient == 13:

        return 100
    

    elif coefficient == 14:

        return 120
    

    elif coefficient == 15:

        return 140
    

    elif coefficient == 16:

        return 160
    

    elif coefficient == 17:

        return 180
    

    elif coefficient == 18:

        return 200
    

    elif coefficient == 19:

        return 220
    

    elif coefficient == 20:



        return 240
    
    

    elif coefficient == 21:



        return 260
    


    elif coefficient == 22:


        return 280
    


    elif coefficient == 23:


        return 300
    


    elif coefficient == 24:


        return 320
    


    elif coefficient == 25:


        return 340
    


    elif coefficient == 26:


        return 360
    


    elif coefficient == 27:


        return 380
    


    elif coefficient == 28:


        return 400
    


    elif coefficient == 29:


        return 420
    


    elif coefficient == 30:


        return 440
    


    elif coefficient == 31:


        return 460
    


    elif coefficient == 32:


        return 480
    


    elif coefficient == 33:


        return 500

    

    else:

        raise ValueError('Energy for RAG must be between 1 and 5')
