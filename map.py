from token_count import TokenCount
SPEED_OF_SE = 512
from containers import Ensemble
from parsers import parse_formulae, divide_formulae
from util.identifiers import Elements, Modalities, Signs
from util.context_mapppers import map_coefficient_to_ctx_size, map_coefficient_to_rag_k, map_document_size_to_n_summary_paragraphs 
from util.runners import RAG, TextRunner, SDXLRunner, SDXLTurboRunner, FluxRunner, LlavaRunner
from filter import PieceFilter, OrbFilter, HouseFilter, CharacterFilter
from reduce import Reduce
import matplotlib.image as mpimg
from PIL import Image


class BiphasicOscillator:


    def __init__(self,
                 formula,
                 ground_state,
                 x_main,
                 x_aux,
                 acceleration,
                 operators,
                 name,
                 element,
                 modality,
                 rank,
                 **kwargs):
        """
        Initializes a BiphasicOscillator object.

        Args:
            formula (str): The formula of the oscillator.
            ground_state (str): The ground state of the oscillator.
            x (float): The x-coordinate of the oscillator.
            y (float): The y-coordinate of the oscillator.
            acceleration (int): The frequency of the oscillator.
            operators (list): A list of operators associated with the oscillator.
            name (str): The name of the oscillator.
            element (str): The element associated with the oscillator.
            modality (str): The modality of the oscillator.
            rank (int): The rank of the oscillator.

        Returns:
            None
        """
        self.formula = formula
        self.ground_state = ground_state
        self.x_aux = x_aux
        self.x_main = x_main
        self.acceleration =acceleration 
        self.operator = operators[0]
        self.name = name
        self.element = element
        self.modality = modality
        self.rank = rank
        self.type = type 

    def _tic(self):
        """
        Retrieves the value of the x attribute by calling the x method.

        Returns:
            The value returned by the x method.
        """
        return self.x_aux()

    
    def _tac(self, x):
        """
        Calculates the output of the oscillator at a given input.

        Args:
            x (float): The input value to the oscillator.

        Returns:
            float: The output value of the oscillator.
        """
        return self.x_main(x, self.operator)
    


    def __call__(self,  local_acceleration):
        """
        Executes the oscillator for the specified number of cycles.

        This method iterates over the specified frequency and calls the `_tic` method to get the input value
        for each cycle. It then calls the `_tac` method with the input value to calculate the output value
        for each cycle. Finally, it returns the output value of the last cycle along with the radiation generated.

        Args:
            local_acceleration (int): The number of cycles to execute the oscillator for.

        Raises:
            ValueError: If the local_acceleration is less than or equal to the current acceleration of the oscillator.

        Returns:
            tuple: A tuple containing the output value of the last cycle and the radiation generated.
                - y (list): The output value of the last cycle.
                - radiation (float): The radiation generated.
        """
    
        y = []
        radiation = 0

        if local_acceleration - self.acceleration < 0: raise ValueError("Oscillator is exhausted.")

        self.acceleration -= local_acceleration

        for _ in range(local_acceleration): 

            x = self._tic()
            y = self._tac(x)
            radiation += len(y)
            y.append(y)

        radiation = radiation * SPEED_OF_SE 

        return y, radiation

    
    def coefficients(self):
        """
        Calculates the coefficients of the oscillator based on the formula.

        Returns:
            list: A list of the coefficients of the oscillator.
        """

        if self.x_main.__class__ == Derivator:

            coff_1 = self.x_main.energy
        
        elif self.x_main.__class__ == Integrator:

            coff_1 = self.x_main.potential
        
        else:

            raise ValueError("The main oscillator must be an integrator or a derivator.")


        if self.x_aux.__class__ == Derivator:

            coff_2 = self.x_aux.energy
        
        elif self.x_aux.__class__ == Integrator:

            coff_2 = self.x_aux.potential
        
        else:

            raise ValueError("The auxiliary oscillator must be an integrator or a derivator.")

        
        return coff_1, coff_2


    def update_coefficients(self, coff_1, coff_2): 
        """
    	A description of the entire function, its parameters, and its return types.
    	"""

        if self.x_main.__class__ == Derivator:

            self.x_main.energy = coff_1
        
        elif self.x_main.__class__ == Integrator:

            self.x_main.potential = coff_1
        
        else:

            raise ValueError("The main oscillator must be an integrator or a derivator.")


        if self.x_aux.__class__ == Derivator:

            self.x_aux.energy = coff_2
        
        elif self.x_aux.__class__ == Integrator:

            self.x_aux.potential = coff_2
        
        else:

            raise ValueError("The auxiliary oscillator must be an integrator or a derivator.")



class TriphasicOscillator:


    def __init__(self,
                 formula,
                 ground_state, 
                 x_main,
                 x_aux_1,
                 x_aux_2,
                 acceleration,
                 operators,
                 name,
                 element,
                 modality,
                 rank,
                 type2=False):
        """
        Initializes a TriphasicOscillator object.

        Args:
            formula (str): The formula of the oscillator.
            ground_state (str): The ground state of the oscillator.
            x (float): The x-coordinate of the oscillator.
            y1 (float): The first y-coordinate of the oscillator.
            y2 (float): The second y-coordinate of the oscillator.
            acceleration (int): The frequency of the oscillator.
            operators (list): A list of operators associated with the oscillator.
            name (str): The name of the oscillator.
            element (str): The element associated with the oscillator.
            modality (str): The modality of the oscillator.
            rank (int): The rank of the oscillator.

        Returns:
            None
        """
           
        self.formula = formula
        self.name = name
        self.element = element
        self.modality = modality
        self.rank = rank
        self.ground_state = ground_state
        self.x_main = x_main
        self.op1 = operators[0]
        self.x_aux_1 = x_aux_1
        self.op2 = operators[1]
        self.x_aux_2 = x_aux_2
        self.acceleration = acceleration
        self.type2 = type2
        self.exhausted = False



    def _tic(self, **kwargs):
        """
        Executes the `_tic` method of the `TriphasicOscillator` class.

        This method is responsible for retrieving the input values for the oscillator.
        It checks the value of the `type2` attribute to determine the input source.
        If `type2` is `False`, it retrieves the auxiliary input value using the `x_aux_1` method
        and calculates the output value using the `x_main` method with `aux_1` and `op1` as arguments.
        If `type2` is `True`, it retrieves the primary input value using the `aux2` method
        and calculates the output value using the `aux1` method with `x` as the argument.

        Parameters:
            **kwargs (dict): Additional keyword arguments.

        Returns:
            y (float): The output value of the oscillator.
        """
        if self.type2 == False:

            aux_1 = self.x_aux_1() 
            y = self.x_main(aux_1, self.op1)
        
        else:
            
            x = self.aux2()
            y = self.aux1(x)
            
        return y
         

    def _tac(self, x, **kwargs):
        """
        Calculates the output value of the oscillator using the given input value and operator.

        Args:
            x (float): The input value for the oscillator.
            **kwargs (dict): Additional keyword arguments.

        Returns:
            float: The output value of the oscillator.
        """ 
        y = self.x_main(x, self.op2)

        return y


    def __call__(self, local_acceleration):
        """
        Executes the oscillator for the specified number of cycles.

        This method iterates over the specified frequency and calls the `_tic` method to get the input value
        for each cycle. It then calls the `_tac` method with the input value to calculate the output value
        for each cycle. Finally, it returns the output value of the last cycle.

        Returns:
            tuple: A tuple containing the output value of the last cycle and the radiation generated.
                - y (list): The output value of the last cycle.
                - radiation (float): The radiation generated.
        """

        y = [] 
        radiation = 0
        if local_acceleration - self.acceleration < 0: raise ValueError("Oscillator is exhausted.")
        self.acceleration -= local_acceleration

        for _ in range(local_acceleration):

            x = self._tic()
            y = self._tac(x)
            radiation += len(y)
            y.append(y)

        radiation = radiation * SPEED_OF_SE 

        return y, radiation


    
    def coefficients(self):
        """
        Calculates the coefficients of the oscillator based on the formula.

        Returns:
            list: A list of the coefficients of the oscillator.
        """

        if self.x_main.__class__ == Derivator:

            coff_1 = self.x_main.energy
        
        elif self.x_main.__class__ == Integrator:

            coff_1 = self.x_main.potential
        
        else:

            raise ValueError("The main oscillator must be an integrator or a derivator.")


        if self.x_aux_1.__class__ == Derivator:

            coff_2 = self.x_aux_1.energy
        
        elif self.x_aux_1.__class__ == Integrator:

            coff_2 = self.x_aux_1.potential
        
        else:

            raise ValueError("The auxiliary oscillator must be an integrator or a derivator.")


        if self.x_aux_2.__class__ == Derivator:

            coff_3 = self.x_aux_2.energy
        
        elif self.x_aux_2.__class__ == Integrator:

            coff_3 = self.x_aux_2.potential
        
        else:

            raise ValueError("The auxiliary oscillator must be an integrator or a derivator.")

        
        return coff_1, coff_2, coff_3

    
    def update_coefficients(self, coff_1, coff_2, coff_3):
        """
        Updates the coefficients of the oscillator based on the new formula.

        Returns:
            list: A list of the updated coefficients of the oscillator.
        """

 
        if self.x_main.__class__ == Derivator:

            self.x_main.energy = coff_1
        
        elif self.x_main.__class__ == Integrator:

            self.x_main.potential = coff_1
        
        else:

            raise ValueError("The main oscillator must be an integrator or a derivator.")


        if self.x_aux.__class__ == Derivator:

            self.x_aux_1.energy = coff_2
        
        elif self.x_aux_1.__class__ == Integrator:

            self.x_aux_1.potential = coff_2
        
        else:

            raise ValueError("The auxiliary oscillator must be an integrator or a derivator.")


        if self.x_aux_2.__class__ == Derivator:

            self.x_aux_2.energy = coff_3
        
        elif self.x_aux_2.__class__ == Integrator:

            self.x_aux_2.potential = coff_3
        
        else:

            raise ValueError("The auxiliary oscillator must be an integrator or a derivator.")




class QuadriphasicOscillator:


    def __init__(self,
                 formula,
                 ground_state, 
                 x1,
                 y1,
                 x2, 
                 y2,
                 acceleration,
                 name,
                 element,
                 modality,
                 rank,
                 switch, 
                local):
        """
        Initializes the QuadriphasicOscillator with the given parameters.
        
        Args:
            formula (str): The formula of the oscillator.
            ground_state (str): The ground state of the oscillator.
            x1 (float): The x-coordinate of the first oscillator.
            y1 (float): The y-coordinate of the first oscillator.
            x2 (float): The x-coordinate of the second oscillator.
            y2 (float): The y-coordinate of the second oscillator.
            acceleration (int): The frequency of the oscillator.
            name (str): The name of the oscillator.
            element (str): The element associated with the oscillator.
            modality (str): The modality of the oscillator.
            rank (int): The rank of the oscillator.
            switch: The switch parameter.
            local: The local parameter.
        
        Returns:
            None
        """
        

        formula_1, formula_2  = divide_formulae(formula)

        ground_state, _, operators = parse_formulae(formula_1)

        x1 = BiphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x_aux = x1, 
                                        x_main = y1, 
                                        acceleration = acceleration, 
                                        operators = operators, 
                                        name=Signs.VOID, 
                                        element=Elements.VOID, 
                                        modality=Modalities.VOID,
                                        rank=rank,
                                        local=local,
                                        )


        ground_state, _, operators = parse_formulae(formula_2)

        x2 = BiphasicOscillator(formula = formula_2, 
                                        ground_state=ground_state, 
                                        x_aux = x1, 
                                        x_main = y1, 
                                        acceleration = acceleration, 
                                        operators = operators, 
                                        name=Signs.VOID, 
                                        element=Elements.VOID, 
                                        modality=Modalities.VOID,
                                        rank=rank,
                                        local=local,
                                        )


        self.formula = formula
        self.ground_state = ground_state
        self.x1 = x1  
        self.x2 = x2
        self.switch = switch 
        self.acceleration = acceleration 
        self.name = name
        self.element = element
        self.modality = modality
        self.rank = rank
        self.local = local
        self.exhausted = False
    




    def _tic(self):
        """
        Retrieves the values of `x1` and `y1` by calling the `x1` and `y1` methods respectively, with `x1` as the input and `op1` as the operator.
        Retrieves the values of `x2` and `y2` by calling the `x2` and `y2` methods respectively, with `x2` as the input and `op3` as the operator.
        Returns a tuple containing the values of `y1` and `y2`.
        """
        y1 = self.x1()
        y2 = self.x2()

        return y1, y2
    

    def _tac(self, x1, x2):
        """
        Calculates the output of the oscillator at a given input.

        Args:
            x1 (float): The first input value to the oscillator.
            x2 (float): The second input value to the oscillator.

        Returns:
            float: The output value of the oscillator.
        """
        y = self.switch(x1=x1, x2=x2) 

        return y
    

    def __call__(self, local_acceleration):
        """
        Executes the oscillator for the specified number of cycles. This method iterates over the specified frequency and calls the `_tic` method to get the input values for each cycle. It then calls the `_tac` method with the input values to calculate the output value for each cycle. Finally, it returns the output values of the last cycle and the radiation generated.
        Args:
            local_acceleration (int): The number of cycles to execute the oscillator for.
        Raises:
            ValueError: If the local_acceleration is less than or equal to the current acceleration of the oscillator.
        Returns:
            tuple: A tuple containing the output values of the last cycle and the radiation generated.
                - y (list): The output values of the last cycle.
                - radiation (float): The radiation generated.
        """
        y = []
        radiation = 0

        if local_acceleration - self.acceleration < 0: raise ValueError("Oscillator is exhausted.")
        self.acceleration -= local_acceleration
        
        for _ in range(local_acceleration):

            x1, x2 = self._tic()
            y = self._tac(x1, x2)
            radiation += len(y)
            y.append(y)


        radiation = radiation * SPEED_OF_SE

        return y, radiation 
    


    def coefficients(self):
        """
        Calculates the coefficients of the oscillator based on the formula.

        Returns:
            list: A list of the coefficients of the oscillator.
        """


        coff1, coff2 = self.x1.coefficients()
        coff3, coff4 = self.x2.coefficients()

        return coff1, coff2, coff3, coff4

    
    def update_coefficients(self, coff_1, coff_2, coff_3, coff_4):

        """
        Updates the coefficients of the oscillator based on the new formula.

        Returns:
            list: A list of the updated coefficients of the oscillator.
        """

        self.x1.update_coefficients(coff_1, coff_2)
        self.x2.update_coefficients(coff_3, coff_4)







class FunctionMapper:

    def summarize(self):

        identity = """
            You are an intelligent agent. Your task is to summarize documents into {number_of_paragraphs} paragraphs.
        """

        prompt = """

            Document:

                {document}

            Answer:

        """

        return identity, prompt

    def ni_se_fixed(self):

        identity =  """

            You are an intelligent agent. Your task is to make plans based on data perceived in the present, aswell as your intentions, narratives and suspicions. You always take present action in relation to what is a viable next step in your own narrative. You turn many observations of the environment into one impression.

        """

        prompt = """
            Narratives:

                {narratives}
            
            Present:

                {environment_data}

            Answer:

            """


        return identity, prompt
   

    def se_ni_fixed(self):

        identity = """

            You are an intelligent agent. Your task is to turn one plan into many actions based on the impressions, intentions and suspicions you have aswell as you can perceive in the present. You always take present action defending what you wan't to do with your own narrative.

        """

        prompt = """
            Narratives:

                {narratives}
            
            Present:

                {environment_data}

            Answer:
        """

        return identity, prompt


    
    def se_si_cardinal(self):

        identity = """

            You are an intelligent agent. Your task is to take action based on present data, and then on what you remember to be similar to what you are currently experiencing. You always take present action seeking to change what you already lived. You use your memories to take many different actions.
        """

        prompt = """

            Memories:

                {memories}


            Present:

                {environment_data}


            Answer:
            """
        
        return identity, prompt


    def si_se_cardinal(self):


        identity =  """

            You are an intelligen agent. Your task is to match your present actions with past perceived senssations. You always take present action seeking to change things in the present so they are sinmilar to the past. 
        """

        prompt = """

            Memories:

                {memories}


            Present:

                {environment_data}


            Answer:

        """

        return identity, prompt



    def ni_fi_orbital(self):

        identity = """

            You are an intelligent agent. Your task is to judge your narratives, intentions and suspicions in accordance to which one is best to your own assesment of importance. You are not a doer, so you always take present action in relation to what maybe will improve your sense of self-importance in the future.
            WDYou always take decisions by making narratives based on what you judge important. Your aim is to be regarded as a person who can make philosophical statements to give everyone future sucesss.
        """

        prompt = """

            Things you find important:

                {important_things}

            Narratives:

                {narratives}


            Answer: 
        """

        return identity, prompt


    def ni_fe_orbital(self):


        identity =  """

            You are an intelligent agent. Your task is to make plans, suspicions and narratives based on what other people think is important. You are not a doer, so you always take present action in relation to what will maybe improve your social esteem in the future.
            You always take decisions by making plans and stories based on what other people judged important. Your aim is to be regarded as an advocate for the sake of everyones future.

        """

        prompt = """
       
            Things other people find important:

                {important_things}

            Narratives:

                {narratives}

            Answer:
        

        """

        return identity, prompt



    def ni_te_orbital(self):


        identity = """

            You are an intelligent agent. Your task is to make plans and suspicions based on rational data and consensus logical thinking. You are not a doer so you always take present action in relation to what will maybe improve your own reputation and capacity in the future. Your aim is to be regarded as a good planner.
            You turn many sources of rational data into one impression that can give progress to your personal narrative.

        """
        prompt = """
            Rational data:

                {rational_data}


            Narratives:

                {narratives}


            Answer:
        """
        
        return identity, prompt
    

    def ni_ti_orbital(self):


        identity = """

            You are an intelligent agent. Your task is to make plans, stories and suspicions on the basis of integrity and logical statements. You are not a doer, so you always take present action in relation to what will maybe improve your capacity to keep acting coherently and with integrity in the future. Your aim is to be regarded as an incorruptible and sound visionary for matters of humanity.

        """

        prompt = """
            Logical data:

                {logical_data}
            

            Narratives: 

                {narratives}


            Answer:
        """ 

        return identity, prompt


    def se_ti_orbital(self):

        identity = """

            You are an intelligent agent. Your task is to take many inmediate actions on the basis of logical statements and whats inmediately verifiable to be true in the environment data. You are not a planner so you always take present action in relation to what will inmediately demonstrate a capacity to behave with common sense in the current situation. Your aim is to be regarded as a quick thinker, a fighter and a quick problem solver who wants to know if the things present are real or not. 
        """

        prompt = """

            Logical data:

                {logical_data}


            Environment data:

                {environment_data}
            
            Answer:
        """


        return identity, prompt


    def se_te_orbital(self):


        identity =  """

            You are an intelligent agent. Your task is to take many inmediate actions on the basis of rational data and quantitative thinking. You are not a planner, so you always take present action in relation to what will inmediately improve your reputation. Your aim is to be regarded as someone who can do anything to achieve success.
        """

        prompt = """
        

            Rational data:

                {rational_data} 

           Environment data:

                {environment_data}             

            Answer:
        """

        return identity, prompt
    

    def se_fi_orbital(self):


        identity =  """

            You are an intelligent agent. Your task is to take many inmediate actions on the basis of what you personally previously found to be important. You are not a planner, so you always take present action in relation to what will inmediately improve your own sense of esteem. Your aim is to be regarded as a good performer who can impose of themselves any role. 

        """

        prompt = """
            Data you find important: 

                {important_data}

            Environment data:

                {environment_data}

            Answer:

        """


        return identity, prompt
    
    def se_fe_orbital(self):


        identity = """

            You are an intelligent agent. Your task is to take many inmediate actions on the basis of what other people find to be important. You are not a planner, so you always take present action in relation to what what will inmediately improve the esteem that other people have on you. Your aim is to be regarded as a fighter and someone who can do anything other people find important.

        """


        prompt = """
            Data other people find important:

                {important_data}

            Environment data:

                {environment_data}

            Answer:

        """


        return identity, prompt


    def si_ne_fixed(self):


        identity = """  
        
            You are an intelligent agent. Your task is to accumulate rich experiences you can later reflect upon. You always take present action by associating past data with present data and replicating what you have experienced in the past.
        """

        prompt = """
            Environment data:

                {environment_data}
            

            Memories:

                {memories}


            Answer:

        """


        return identity, prompt
    

    def ne_si_fixed(self):


        identity = """  

            You are an intelligent agent. Your task is to reflect upon things based on previous experience. You always take present action by extrapolating present data and past data, and coming up with novel hypotheticals from past experiences.

        """

        prompt = """

            Environment data:

                {environment_data}


            Memories:

                {memories}


            Answer:
        """

        return identity, prompt
        
    
    def si_ti_orbital(self):


        identity = """  

            You are an intelligent agent. Your task is to review past memories and produce logical statements out of these experiences on the basis of what you already know to be true. You always take present action by remembering and logically ordering what you have seen in the past. Your aim is to be regarded as someone whos reliable, stable, steady and aware of old and common sense truths.
        """

        prompt = """
            Memories:

               {memorized_data}


            Logical data:

                {logical_data}
 
            Answer:

        """


        return identity, prompt


    def si_te_orbital(self):


        identity =  """

            You are an intelligent agent. Your task is to review past memories and produce many rational statements out of these data. You always take present action by remembering and doing a rational or quantitative analysis of what you have seen in the past. Your aim is to be regarded as someone whos capable, reputable and whos knowdledgeable of many things in the world.

        """

        prompt = """
            Rational data:

                {rational_data}


            Memories:

                {memories}


            Answer:

        """

        return identity, prompt
    

    def si_fi_orbital(self):


        identity = """

           You are an intelligent agent. Your task is to review past memories data and produce value and importance judgements out of these data, on the basis of importance. You always take present action by doing an importance analysis of what you have seen in the past. Your aim is to order what you personally find to be important and be regarded as someone whos very aware of tradition and their own moral compass.
        """

        prompt = """

            Memories:

                {memorized_data}


            Data you find important:

                {important_data}

            Answer:

        """


        return identity, prompt


    def si_fe_orbital(self):


        identity = """
            You are an intelligent agent. Your task is to review past memories and produce many judgements of these data on the basis of what other people find to be important. You always take present action by remembeing past experience and assesing what other people find important. Your aim is to be regarded as someone who mantains social stability and defends the interests of others. 
        """

        prompt = """
            Memories:

                {memories}


            Things other people find important:

                {important_things}

            Answer:

        """


        return identity, prompt


    def ne_ti_orbital(self):

        identity = """

            You are an intelligent agent. Your task is to extrapolate present data with past memories and produce many logical statements of these data. You always take present action by extrapolating past memories with new hypothetical situations, and judging how these new hyphoteticals fit with what you are currently experiencing. Your aim is to be regarded as a quick thinker and someone whos inventive.
        
        """
        prompt = """
         
            Logical data:

                {logical_data}

            Environment data:

                {environment_data}

            Answer:

        """

        return identity, prompt
    

    def ne_fi_orbital(self):

        identity =  """

            You are an intelligent agent. Your task is to extrapolate present data with past memories and produce many importance judgements of these on the basis of personal preference and sense of personal importance. You always take present action by extrapolating past memories with new hypothetical situations, and judging how these new hyphoteticals fit with what you are currently experiencing. Your aim is to be regarded as a person who can advise and imaginate whats necessary for success. 
        """

        prompt = """
 
            
            Data you find important:

                {important_data}

            Environment data:

                {environment_data}

            Answer:

        """

        return identity, prompt

    def ne_te_orbital(self):

        identity = """

            You are an intelligent agent. Your task is to extrapolate present data with past memories and produce many rational judgements of these on the basis of quantitative thinking and rationality. You always take present action by extrapolating past memories with new hypothetical situations, and judging how these new hyphoteticals fit with what you are currently experiencing. Your aim is to be regarded as a person who easily advises whats necessary for success.
        """

        prompt = """  

            Rational data:

                {rational_data}

            Environment data:    

                {environment_data}

            Answer:

        """

        return identity, prompt
    

    def ne_fe_orbital(self):

        identity = """

            You are an intelligent agent. Your task is to extrapolate present data and produce many judgements of these data on the basis of what other people find important. You always take present action by extrapolating past memories with new hypothetical situations, and judging how these new hyphoteticals fit with what you are currently experiencing. Your aim is to be regarded highly as an imaginative person who can easily picture what other people find important and advise them on the basis of this.
        """


        prompt = """ 

            Things other people find important:

                {important_things}

            
            Environment data:

                {environment_data}

            Answer:

        """


        return identity, prompt

    
    def fi_te_fixed(self):

        identity = """
            You are an intelligent agent. Your task is to take inmediate action on the basis of what you find important. Your aim is to be regarded as a reputable and important person.
        """

        prompt = """
            Things you find important:

                {important_things}
            
            Rational data:

                {rational_data}

            Answer:
        """


        return identity, prompt

    def te_fi_fixed(self):

        identity =  """
            You are an intelligent agent. Your task is to take  action on the basis of whats rational and logically verfiable by many sources. Your aim is to improve your own sense of esteem by measure of what you believe to be important.
        """
        prompt = """
            Rational data:

                {rational_data}


            Things you find important:

                {important_things}

            Answer:
        """
        

        return identity, prompt
    
    def fi_fe_cardinal(self):

        idenityty =  """
            You are an intelligent agent. Your task is to take inmediate action on the basis of changing the beliefs of other people about you. Your aim is to do things that improve your own esteem.
        """
        prompt = """
            Things you personally find important:

                {important_things}
            

            Things other people find important:

                {external_important_things}

            Answer:

        """

        return idenityty, prompt
    

    def fe_fi_cardinal(self):

        identity = """

            You are an intelligent agent. Your task is to communicate on the basis of changing your own beliefs about yourself. Your aim is to do things that make other people regard you higher. You produce many statements about things other people find important.
        """

        prompt = """


            Things you personally find important:

                {important_things}
            

            Things other people find important:

                {external_important_things}

            Answer:

        """

        return identity, prompt


    def ti_fe_fixed(self):

        identity = """

            You are an intelliget agent. Your task is to take inmediate action on the basis of what you find logical and verified to be true. Your aim is to do things that make other people regard you higher by the measure of your soundness and thinking and how your talent as a thinker make others feel better.
        """
        prompt =  """


            Things you know to be true:

                {logical_data}

            Things other people find important:

                {external_important_things}

            Answer:

        """ 

        return identity, prompt


    def fe_ti_fixed(self):

        identity = """

            You are an intelligent agent. Your task is to communicate many statements on the basis of what other people find important. Your aim is to do things that make other people regard you higher by the way in which you logicallly make compromises that make everyone happy and show your ability to think logically.  
        """

        prompt =  """


            Things other people find important:

                {external_important_things}

            Things you know to be true:

                {logical_data}

            Answer:

        """ 


        return identity, prompt
    
    def fi_se_orbital(self):

        identity = """

            You are an intelligent agent. Your task is to take inmediate action on the basis of what you personally find important. You analyze data from the present environment and take decisions on the basis of what is important to you. Your aim is to  be regarded as a capable performer, always ready to improvise and take the stage.
        """ 
        prompt = """
            Things you find important:
            

                {important_things}

            Environment data:

                {environment_data}

            Answer:

        """

        return identity, prompt


    def fi_ne_orbital(self):

        identity = """

            You are an intelligent agent. Your task is to take inmediate action on the basis of what you personally find important. You analyze current data, and yuxtapose it with past memories to extrapolate hypotheticals of what could happen. Your aim is to judge this hypotheticals on the basis of whats important to you and be regarded as a rich fantasist.
        """

        prompt = """
            Things you find important:

                {important_things}

            Environment data:

                {environment_data}

            Answer:
        """
        

        return identity, prompt


    def fi_si_orbital(self):

        identity =  """  
            You are an intelligent agent. Your task is to judge past memories on the basis of what you personally find important. You analyze your past memories and order them on the basis of what is important to you. Your aim is to be regarded as a person with deeply seated moral values.
        """

        prompt = """

            Things you find important:

                {important_things}

            Memories:

                {memories}

            Answer:
        """


        return identity, prompt

    def fi_ni_orbital(self):

        identity = """ 

            You are an intelligent agent. Your task is to order by importance your personal narratives, suspicions and intentions on the basis of what you personally find important. You analyze your intuitions and intentions and order them on the basis of what is important to you. Your aim is to be regarded as a person with a rich imagination.
        """

        prompt = """

            Things you find important:

                {important_things}

            Narratives:

                {narratives}

        """


        return identity, prompt


    def te_ni_orbital(self):
        
        identity =  """

            You are an intelligent agent. Your task is to analyze rational data and make many plans and strategic narratives on the basis of what many sources have verified to be true. You always act by communicating your plans and justifying them with rational data. Your aim is to be regarded a capable leader whos able to command and manage resources into future sucess.

        """
    
        prompt = """
            Narratives:

                {narratives}

            Rational data:

                {rational_data}

            Answer:
        """


        return identity, prompt

    
    def te_ne_orbital(self):

        identity =  """  

            You are an intelligent agent. Your task is to gather and produce rational data and yuxtapose it with present experience extrapolating hypotheticals on what could happen next. You state many hypotheticals on the basis of rationality, You always take present action by communicating directives on the basis of what could happen next. Your aim is to be regarded as a reputable preparationist whos prepared for any contigency before it happens.
        """

        prompt = """
            Environment data:

                {environment_data}
                        

            Rational data:

                {rational_data}
      
            Answer:
        """


        return identity, prompt


    def te_se_orbital(self):

        identity =  """

            You are an intelligent agent. Your task is to gather and produce rational data and use it to judge present experience. You always take present action by communicating many directives of whats rational and whats not. Your aim is to be regarded as an individual who can make order and decisions out of any chaotic situation.

        """

        prompt ="""
            Environment data:

                {environment_data}

            Rational data:

                {rational_data}

            Answer:
        """
        

        return identity, prompt


    def te_si_orbital(self):

        identity = """

            You are an intelligent agent. Your task is to gather and produce rational data and use it to judge past memories. You always take present action by communicating many directives of whats rational and wahts not in relation of past memories. Your aim is to be regarded as a reputable individual well prepared for all past challenges.
        """

        prompt = """

            Memories:

                {memories}

            Rational data:

                {rational_data}

            Answer:

        """

        return identity, prompt


    def fe_se_orbital(self):

        identity = """

            You are an intelligent agent. Your task is to gather and produce many statements of what other people find important and use it to judge present experience. You always take present action by communicating directives of whats important to everyone in the present situation and what not. Your task is to be an individual always regarded highly as a protagonist in the present situation.
        """


        prompt = """

            Environment data:

                {environment_data}

            Data other people find important:

                {important_data}

            Answer:

        """


        return identity, prompt


    def fe_ni_orbital(self):


        identity  = """  

            You are an intelligent agent. Your task is to gather and produce many statements of what other people find important and use it to judge what you think will likely happen. You always take action by ordering suspicions, narratives and communicating directives on the basis of what other people find important and what you supect will happen later on. Your aim is to be a visionary leader on matters of social importance.
        """

        prompt = """    

            Narratives:

                {narratives}

            Data other people find important:

                {important_data}

            Answer:

        """


        return identity, prompt

    def fe_si_orbital(self):


        identity  =  """  

            You are an intelligent agent. Your task is to gather and produce many statements of what other people find important and use it to judge past experience. You always take action by ordering past memories and communicating directives on the basis of what other people find important and what you have already seen happening. Your aim is to be a person always prepared for any situation involving the desires ofother people.

        """

        prompt =  """

            Memories:

                {memories}

            Data other people find important:

                {important_data}

            Answer:
         
        """


        return identity, prompt
        


    def fe_ne_orbital(self):


        identity = """      

            You are an intelligent agent. Your task is to gather and produce many statements of what other people find important and use it to judge hypotheticals. You always take action by yuxtaposing previous experience with present experience hypothetizing likely scenarios, and communicating directives on the basis of what other people find important and what you perceive could likely happen. Your aim is to be an individual who knows what other people want before they know it.
        """


        prompt = """

            Environment data:

                {environment_data}
 

            Data other people find important:

                {important_data}    

            Answer: 
        """


        return identity, prompt

    
    def ti_si_fixed(self):

        identity = """

            You are an intelligent agent. Your task is to logically assess data and produce logical statements of your past memories. You always take present action by logically ordering and judging past memories. Your aim is to be regarded as an accurate logician.
        """

        prompt = """

            Memories:

                {memories}
            
            
            Logical statements:

                {logical_statements}

            Answer:

        """


        return identity, prompt


    def ti_se_fixed(self):


        identity = """

            You are an intelligent agent. Your task is to analyze data from the environment and order it on the basis of what you know to be true. You always take present action by judging wether or not the present data is true or not. Your aim is to be regarded as a quick thinker who wants to figure out wether things can be done in the inmediate present or not.

        """ 
        prompt = """
            Environment data:

                {environment_data}
            
            Logical statements:

                {logical_statements}

            Answer:

        """

        return identity, prompt
    
    def ti_ni_fixed(self):


        identity = """

            You are an intelligent agent. Your task is to analyze your impressions, suspicions and narratives and order them on the basis of what you know to be true. You always take present action by judging wether or not your intuitions are true or not. Your aim is to be regarded as someone who can make sound tactical plans out of problems in the present situation. You turn entitiy definitions into inmediate plans you are going to execute.
        """

        prompt = """

            Narratives:

                {narratives}
            
            Logical statements:

                {logical_statements}

            Answer:


        """

        return identity, prompt
    

    def ti_ne_fixed(self):


        identity = """  

            You are an intelligent agent. Your task is to yuxtapoose present data with past data, make hypothetical scenarios and analyze these hypotheticals ordering them on the basis of what you know to be true. You always take present action by judging wether or not the hypothetical data is true or not. Your aim is to be regarded as someone with a sound scientific mindset.
        """

        prompt = """
     
            Logical statements:

                {logical_statements}

            Environment data:

                {environment_data}

            Answer:

        """

        return identity, prompt
    
    def ti(self):


        identity = """

            You are an intelligent agent. Your task is to make logical conclusions.
        """

        prompt = """
            Logical statements:

                {logical_statements}

            Answer:

        """ 

        return identity, prompt


    def te(self):

        identity = """ You are an intelligent agent. Your task is to make rational many decisions based on previous rational statements and current data. Your task is to express organizational directives backed by rational data. """

        prompt = """
            Current rational data:

                {rational_data}

            Answer:

        """

        return identity, prompt

                 
    def fi(self):


        identity =  """

            You are an intelligent agent. Your task is to make an important decision on the basis of what you think is important. You categorize information on the basis of it being important to you or not. 
        """
        prompt = """

            Thins you find important:

                {important_data}

            Answer:

        """

        return identity, prompt


    def fe(self):

        identity = """ 

            You are an intelligent agent. Your task is to make many decisions and express them, on the basis of what everyone think is important. You lead peoples opinion.

        """
        prompt = """
            Things you find important:

                {important_data}    

            Answer:
        """

        return identity, prompt
    

    def se(self):


        identity = """

            You are an intelligent agent. Your task is to take many inmediateactions on the basis on what you can observe from the inmediate environment.  Your goal is to make fast and inmediate change.
        """

        prompt = """
            Environment data:

                {environment_data}

            Answer:

        """

        return identity, prompt

 


    def ni(self):


        identity = """

            You are an intelligent agent. Your task is to extract the relationships between entities in the narrative from either an impresion of an image or a document. Answer with just the relationships.

        """

        prompt = """ 
            Previous narratives:

                {narratives}


            Answer:

        """

        return identity, prompt

    
    def ns(self):


        identity = """

            You are an intelligent agent. Your task is to take action preparing for the future when data points at everyone reacting to the present. If everyone is already preparing for the future you act preparing for the future but reminding everyone that the future is important.
        """

        prompt = """

            Data about the future:

                {data_about_the_future}

            Data about the present:

                {data_about_the_present}

            Answer:

        """


        return identity, prompt


    def sn(self):


        identity =  """

            You are an intelligent agent. Your task is to take action acting on the present when data points at things being too concerned to the future. If everyone is already acting on the present you act on the present but reminding everyone that the present is important.
        """

        prompt = """

            Data about the future:

                {data_about_the_future}

            Data about the present:

                {data_about_the_present}

            Answer:

        """


        return identity, prompt


    def tf(self):

        identity = """

            You are an intelligent agent. Your task is to take decisions logically when everyone is currently thinking emotionally. If everyone is thinking logically already you take logical decisions reminding everyone that emotions are important.
        """


        prompt = """

            Logical statements:

                {logical_statements}


            Emotional statements:

                {emotional_statements}

            Answer:

        """


        return identity, prompt


    def ft(self):

        identity = """
            You are an intelligent agent. Your task is to take decisions emotionally when everyone is currently thinking logically. If everyone is thinking emotionally already you take emotional decisions but reminding everyone that Logical statements are important.

        """

        prompt = """

            Emotional statements: 

                {emotional_statements}


            Logical statements:

                {logical_statements}

            Answer:

        """

        return identity, prompt




db = FunctionMapper()

class Derivator:
    def __init__(self, domain, energy, mass_energy, runners_map, **kwargs) -> None:
        """
        Initializes a new instance of the class with the given domain, energy, and mass-energy.

        Args:
            domain (str): The domain of the object.
            energy (float): The energy of the object.
            mass_energy (float): The mass-energy relation of the object.

        Returns:
            None """

        self.domain = domain.upper()
        self.mass_energy = mass_energy
        self.energy = energy 
        self.runners_map = runners_map
        
        if 'namespace' in kwargs.keys():

            self.namespace = kwargs['namespace']

        if 'local' in kwargs.keys():

            self.local = kwargs['local']
        
        if 'symbol' in kwargs.keys():

            self.symbol = kwargs['symbol']


        tc = TokenCount(model_name="gpt-3.5-turbo")



        if (self.runners_map[self.domain] == 'LLAMA8B'  or self.runners_map[self.domain] == 'LLAMA70B')and tc.num_tokens_from_string(mass_energy) > (self.energy):

            n_paragraphs = map_document_size_to_n_summary_paragraphs('LLAMA', self.energy)
        
        elif self.runners_map[self.domain] == 'PHI_MINI' and tc.num_tokens_from_string(mass_energy) > (self.energy):

            n_paragraphs = map_document_size_to_n_summary_paragraphs('PHI', self.energy)

        else:

            raise ValueError('Energy number for {} must be between 1 and 12'.format(self.domain))

        
        identity, prompt = db.summarize()
        prompt = prompt.format(document=self.mass_energy)
        identity = identity.format(number_of_paragraphs=n_paragraphs)
        summarizer = TextRunner(local=self.local, ctx_size=130000, **self.runners_map)
        self.mass_energy  = summarizer(prompt, identity)
     


    def __call__(self, **kwargs):
       
    
        if 'op' in kwargs.keys():

            op = kwargs['op1']
            x = kwargs['x']

            if op == '~':


                if self.runners_map['JOINT'].upper() == 'LLAMA8B':

                    ctx_size = map_coefficient_to_ctx_size(self.energy)
                    Joint = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)
                else:

                    raise ValueError('Invalid joint runner')


                if self.symbol == 'Se':
  
                    if self.runners_map['SE'].upper() == 'LLAMA8B':

                        ctx_size = (self.energy) 
                        Se =  TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)
                    
                    else:

                        raise ValueError('Invalid se runner')   


                    identity, prompt = db.se()
                    prompt = prompt.format(environment_data=self.mass_energy)
                    Se_source = Se(identity, prompt)


                    if self.runners_map['JOINT'].upper() == 'LLAMA8B':

                        ctx_size = (self.energy)
                        Joint = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)


                    else:

                        raise ValueError('Invalid joint runner')

                        
                    if x.symbol == 'Fi': 

                        Fi_sink = x
                        identity, prompt = db.se_fi_orbital()
                        prompt.format(environment_data=Se_source, important_data = Fi_sink)

                        y = Joint(identity, prompt)

                        return y


                    elif x.symbol == 'Te':
                        
                        Te_source = x
                        identity, prompt = db.se_te_orbital()
                        prompt.format(environment_data=Se_source, ration_data = Te_source)

                        y = Joint(identity, prompt)

                        return y


                    elif x.symbol == 'Ti':

                        Ti_sink = x
                        identity, prompt = db.se_ti_orbital()
                        prompt.format(environment_data=Se_source, logical_data = Ti_sink)

                        y = Joint(identity, prompt)

                        return y


                    elif x.symbol == 'Fe':

                        Fe_source = x
                        identity, prompt = db.se_fe_orbital()
                        prompt.format(environment_data=Se_source, important_data = Fe_source)

                        y = Joint(identity, prompt)

                        return y

                    else:

                        raise ValueError('Wrong operator: ' + op) 


                elif self.symbol == 'Ne':
                     

                    Ne = RAG()

                    k = map_coefficient_to_rag_k(self.energy)
                    Ne_source = Ne(collection=self.namespace, 
                        k_value=k,
                        hallucinate=True,
                        document=self.mass_energy) 

              
                    if x.symbol == 'Fi':
                        
                        Fi_sink = x
                        identity, prompt = db.ne_fi_orbital()
                        prompt.format(environment_data=Ne_source, important_data = Fi_sink)

                        y = Joint(identity, prompt)

                        return y
                    

                    elif x.symbol == 'Te':

                        Te_source = x
                        identity, prompt = db.ne_te_orbital()
                        prompt.format(environment_data=Ne_source, important_data = Te_source)

                        y = Joint(identity, prompt)

                        return y


                    elif x.symbol == 'Ti':

                        Ti_sink = x
                        identity, prompt = db.ne_ti_orbital()
                        prompt.format(environment_data=Ne_source, logical_data = Ti_sink)

                        y = Joint(identity, prompt)

                        return y


                    elif x.symbol == 'Fe':

                        Fe_source = x
                        identity, prompt = db.ne_fe_orbital()
                        prompt.format(environment_data=Ne_source, important_data = Fe_source)

                        y = Joint(identity, prompt)

                        return y
                    

                    else:

                        raise ValueError('Wrong operator: ' + op)


                elif self.symbol == 'Fe':
                                       

                    identity, prompt = db.fe()
                    prompt = prompt.format(important_data=self.mass_energy)

                    if self.runners_map['F'].upper() == 'LLAMA8B':

                        ctx_size = (self.energy) 
                        Fe =  TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)

          
         
                    else:

                        raise ValueError('Wrong runner.') 
                                        
                    
                    Fe_source = Fe(identity, prompt)



                    if x.symbol == 'Se':

                        Se_source = x
                        identity, prompt = db.fe_se_orbital()
                        prompt.format(environment_data=Se_source, important_data = Fe_source)

                        y = Joint(identity, prompt)

                        return y
                    
                    elif x.symbol == 'Ne':

                        Ne_source = x
                        identity, prompt = db.fe_ne_orbital()
                        prompt.format(environment_data=Ne_source, important_data = Fe_source)

                        y = Joint(identity, prompt)

                        return y
                    

                    elif x.symbol == 'Ni':

                        Ni_sink = x
                        identity, prompt = db.fe_ni_orbital()
                        prompt.format(important_data = Fe_source, narratives = Ni_sink)

                        y = Joint(identity, prompt)

                        return y

                    
                    elif x.symbol == 'Si':

                        Si_sink = x
                        identity, prompt = db.fe_si_orbital()
                        prompt.format(important_data =Fe_source, memories = Si_sink)

                        y = Joint(identity, prompt)

                        return y

 

                elif self.symbol == 'Te':

                                  
                    ctx_size = (self.energy) 

                    identity, prompt = db.te()
                    prompt = prompt.format(environment_data=self.mass_energy)

                  

                    if self.runners_map['T'].upper() == 'LLAMA8B':

                        Te =  TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)

               

                    else:

                        raise ValueError('Wrong runner.')

                    
                    Te_source = Te(identity, prompt)


                    if x.symbol == 'Ni':

                        Ni_sink = x
                        identity, prompt = db.te_ni_orbital()
                        prompt.format(rational_data = Te_source, narratives = Ni_sink)

                        y = Joint(identity, prompt)

                        return y
                    
                    elif x.symbol == 'Si':

                        Si_sink = x
                        identity, prompt = db.te_si_orbital()
                        prompt.format(rational_data = Te_source, memories = Si_sink)

                        y = Joint(identity, prompt)

                        return y
                    

                    elif x.symbol == 'Se':

                        Se_source = x
                        identity, prompt = db.te_se_orbital()
                        prompt.format(rational_data = Te_source, environment_data = Se_source)

                        y = Joint(identity, prompt)

                        return y
                    
                    elif x.symbol == 'Ne':

                        Ne_source = x
                        identity, prompt = db.te_ne_orbital()
                        prompt.format(rational_data = Te_source, environment_data = Ne_source)

                        y = Joint(identity, prompt)

                        return y
                
                    else:

                        raise ValueError('Wrong operator: ' + op)

            
            elif op == 'oo':

                if self.symbol == 'Se':


                    identity, prompt = db.se()
                    prompt = prompt.format(environment_data=self.mass_energy)

                    if self.runners_map['S'].upper() == 'LLAMA8B':

                        ctx_size = (self.energy) 
                        Se =  TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)

                    else:

                        raise ValueError('Wrong runner.')


                    Se_source = Se(identity, prompt)

                    Si_sink = x

                    if self.runners_map['JOINT'].upper() == 'LLAMA8B':

                        ctx_size = (self.energy)
                        Se_Si = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)

                    else:  

                        raise ValueError('Wrong runner.')

                    
                    identity, prompt = db.se_si_cardinal()
                    prompt.format(environment_data = Se_source, memories = Si_sink)

                    y = Se_Si(identity, prompt)

                    return y
                

                elif self.symbol == 'Ne':


                    identity, prompt = db.ne()
                    prompt = prompt.format(environment_data=self.mass_energy)



                    if self.runners_map['N'].upper() == 'LLAMA8B':

                        ctx_size = (self.energy)
                        Ne = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)

                    else:  

                        raise ValueError('Wrong runner.') 

                    Ne_source = Ne(identity, prompt)
                    Ni_sink = x

                    if self.runners_map['JOINT'].upper() == 'LLAMA8B':

                        ctx_size = (self.energy)
                        Ne_Ni = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)

                    else:  

                        raise ValueError('Wrong runner.')


                    identity, prompt = db.ne_ni_cardinal()
                    prompt.format(environment_data = Ne_source, narratives = Ni_sink)

                    y = Ne_Ni(identity, prompt)

                    return y

                
                elif self.symbol == 'Te':


                    identity, prompt = db.te()
                    prompt = prompt.format(rational_data=self.mass_energy)

                    if self.runners_map['T'].upper() == 'LLAMA8B':

                        ctx_size = (self.energy)
                        Te = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)

                    else:   

                        raise ValueError('Wrong runner.')

                    
                    Te_source = Te(identity, prompt)
                    Ti_sink = x

                    if self.runners_map['JOINT'].upper() == 'LLAMA8B':

                        ctx_size = (self.energy)
                        Te_Ti = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)


                 
                    else:

                        raise ValueError('Wrong runner.')



                    identity, prompt = db.te_ti_cardinal()
                    prompt.format(rational_data = Te_source, logical_data = Ti_sink)

                    y = Te_Ti(identity, prompt)

                    return y


                elif self.symbol == 'Fe':


                    identity, prompt = db.fe()
                    prompt = prompt.format(important_things=self.mass_energy)


                    if self.runners_map['F'].upper() == 'LLAMA8B':

                        ctx_size = (self.energy)
                        Fe = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map) 

                    else:

                        raise ValueError('Wrong runner.')


                    Fe_source = Fe(identity, prompt)

                    Fi_sink = x
                    Fe_Fi = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)
                    identity, prompt = db.fe_fi_cardinal()
                    prompt.format(external_important_things = Fe_source, important_things = Fi_sink)

                    y = Fe_Fi(identity, prompt)

                    return y
                
                else:

                    raise ValueError('Wrong cardinal operands')



            elif op == '->':


                if self.symbol == 'Se':

                    ctx_size = (self.energy) 

                    identity, prompt = db.se()
                    prompt = prompt.format(environment_data=self.mass_energy)

         
                    if self.runners_map['S'].upper() == 'LLAMA8B':

                        ctx_size = (self.energy)
                        Se = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)


                    else:  

                        raise ValueError('Wrong runner.')


                    Se_source = Se(identity, prompt)
                    Ni_sink = x

    
                    if self.runners_map['JOINT'].upper() == 'LLAMA8B':

                        ctx_size = (self.energy)
                        Se_Ni = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)


                    else:

                        raise ValueError('Wrong runner.')


                    identity, prompt = db.se_ni_fixed() 
                    prompt.format(environment_data = Se_source, narratives = Ni_sink)

                    y = Se_Ni(identity, prompt)

                    return y
                
                elif self.symbol == 'Ne':


                    identity, prompt = db.ne()
                    prompt = prompt.format(environment_data=self.mass_energy)

                    if self.runners_map['N'].upper() == 'LLAMA8B':

                        ctx_size = (self.energy)
                        Ne = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)


                    else:       

                        raise ValueError('Wrong runner.')


                    Ne_source = Ne(identity, prompt)

                    Si_sink = x

                    if self.runners_map['JOINT'].upper() == 'LLAMA8B':

                        ctx_size = (self.energy)
                        Ne_Si = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)

                    identity, prompt = db.ne_si_fixed() 
                    prompt.format(environment_data = Ne_source, memories = Si_sink)

                    y = Ne_Si(identity, prompt)

                    return y


                elif self.symbol == 'Te':


                    identity, prompt = db.te()
                    prompt = prompt.format(rational_data=self.mass_energy)


                    if self.runners_map['T'].upper() == 'LLAMA8B':

                        ctx_size = (self.energy)
                        Te = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)


                    else:

                        raise ValueError('Wrong runner.')


                    Te_source = Te(identity, prompt)

                    Fi_sink = x

     
                    if self.runners_map['JOINT'].upper() == 'LLAMA8B':

                        ctx_size = (self.energy)
                        Te_Fi = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)

                    else:

                        raise ValueError('Wrong runner.')


                    identity, prompt = db.te_fi_fixed() 
                    prompt.format(rational_data = Te_source, important_things = Fi_sink)

                    y = Te_Fi(identity, prompt)

                    return y
                
                elif self.symbol == 'Fe':


                    identity, prompt = db.fe()
                    prompt = prompt.format(important_data=self.mass_energy)

                    if self.runners_map['F'].upper() == 'LLAMA8B':

                        ctx_size = (self.energy)
                        Fe = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)

                    else:

                        raise ValueError('Wrong runner.')

                        
                    Fe_source = Fe(identity, prompt)

                    Ti_sink = x

                    if self.runners_map['JOINT'].upper() == 'LLAMA8B':

                        ctx_size = (self.energy)
                        Fe_Ti = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)

                    else:

                        raise ValueError('Wrong runner.')                    


                    identity, prompt = db.fe_ti_fixed() 
                    prompt.format(important_data = Fe_source, logical_data = Ti_sink)

                    y = Fe_Ti(identity, prompt)

                    return y


            else:

                raise ValueError('Wrong operator: ' + op)


        elif self.domain == 'N' and 'op1' not in kwargs.keys():

            Ne = RAG()
            k = map_coefficient_to_rag_k(self.energy)

            y = Ne(collection=self.namespace, 
                k_value=k,
                hallucinate=True,
                document=self.mass_energy) 

            return y

            
        elif self.domain == 'S' and 'op1' not in kwargs.keys():

            identity, prompt = db.se()
            prompt = prompt.format(environment_data=self.mass_energy)
            
        
            if self.runners_map['S'].upper() == 'LLAMA8B':

                ctx_size = (self.energy)
                Se = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)

            else:

                raise ValueError('Wrong runner.')


            y = Se(identity, prompt)

            return y
            

        elif self.domain == 'F' and 'op1' not in kwargs.keys(): 
            
            identity, prompt = db.fe()
            prompt = prompt.format(important_data=self.mass_energy)

            if self.runners_map['F'].upper() == 'LLAMA8B':

                ctx_size = (self.energy)
                Fe = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)
            
   
            else:

                raise ValueError('Wrong runner.')


            y = Fe(identity, prompt)

            return y


        elif self.domain == 'T' and 'op1' not in kwargs.keys(): 
 
            identity, prompt = prompt.format(rational_data=self.mass_energy)


            if self.runners_map['T'].upper() == 'LLAMA8B':

                ctx_size = (self.energy)
                Te = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)


  
            else:

                raise ValueError('Wrong runner.')


            y = Te(identity, prompt)

            return y
        

        elif self.domain == '1':

            identity, prompt = db.one()

            if self.runners_map['1'].upper() == 'LLAMA8B':

                ctx_size = (self.energy)
                ex = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)

            else:

                raise ValueError('Wrong runner.')
 

            x = kwargs['x']

            prompt = prompt.format(environment_data=x)
            
            y = ex(identity, prompt)

            return y
       
        elif self.domain == '4':

            identity, prompt = db.four()

            if self.runners_map['4'].upper() == 'LLAMA8B':

                ctx_size = (self.energy)
                ex = TextRunner(local=self.local, ctx_size=ctx_size,     **self.runners_map)

            else:

                raise ValueError('Wrong runner.')
        

            x = kwargs['x']

            prompt = prompt.format(environment_data=x)

            y = ex(identity, prompt)

            return y
    

        elif self.domain == '7':

            identity, prompt = db.seven()

            if self.runners_map['7'].upper() == 'LLAMA8B':

                ctx_size = (self.energy)
                ex = TextRunner(local=self.local, ctx_size=ctx_size,     **self.runners_map)
            else:

                raise ValueError('Wrong runner.')
            


            x = kwargs['x']

            prompt = prompt.format(environment_data=x)

            y = ex(identity, prompt)

            return y

       
        elif self.domain == '10': 


            identity, prompt = db.ten()

            if self.runners_map['10'].upper() == 'LLAMA8B':

                ctx_size = (self.energy)
                ex = TextRunner(local=self.local, ctx_size=ctx_size,     **self.runners_map)
            else:

                raise ValueError('Wrong runner.')

            x = kwargs['x']

            prompt = prompt.format(environment_data=x)

            y = ex(identity, prompt)

            return y
        


        else:

            raise ValueError('Domain must be N, S, F, or T')


from runners import ImageRunner, TextRunner

class Integrator:


    def __init__(self, domain, potential, mass_energy, runners_map, **kwargs) -> None:
        """
        Initializes a new instance of the class with the given domain, potential, and mass energy.

        Args:
            domain (str): The domain of the object.
            potential (float): The potential of the object.
            mass_energy (float): The mass energy of the object.
            **kwargs (dict): Additional keyword arguments.
                namespace (str): The namespace of the object.
                local (bool): Whether the object is local or not.
                symbol (str): The symbol of the object.

        Returns:
            None
        """

        self.domain = domain.upper()
        self.potential = potential
        self.mass_energy = mass_energy
        self.runners_map = runners_map
    

        if 'namespace' in kwargs.keys():

            self.namespace = kwargs['namespace']

        if 'local' in kwargs.keys():

            self.local = kwargs['local']

        if 'symbol' in kwargs.keys():

            self.symbol = kwargs['symbol']



        tc = TokenCount(model_name="gpt-3.5-turbo")

        if (self.runners_map[self.domain] == 'LLAMA8B'  or self.runners_map[self.domain] == 'LLAMA70B')and tc.num_tokens_from_string(mass_energy) > (self.potential):

            n_paragraphs = map_document_size_to_n_summary_paragraphs('LLAMA', self.potential)
    
        else:

            raise ValueError('Potential number for {} must be between 1 and 12'.format(self.domain))

        
        identity, prompt = db.summarize()
        prompt = prompt.format(document=self.mass_energy)
        identity = identity.format(number_of_paragraphs=n_paragraphs)
        summarizer = TextRunner(local=self.local, ctx_size=130000)
        self.mass_energy  = summarizer(prompt, identity)
     




    def __call__(self, **kwargs):


        x = kwargs['x'] 

        if self.domain == 'N' and 'op1' not in kwargs.keys():

            if self.runners_map['N'].upper() == 'LLAMA8B':

                ctx_size = (self.potential)
                Ni = ImageRunner(low_power=False)

            else:

                raise ValueError('Wrong runner.')


            identity, prompt = db.ni()
            prompt = prompt.format(narratives=self.mass_energy)
            y = Ni(prompt)
                
            return y

            
        elif self.domain == 'S' and 'op1' not in kwargs.keys():

            Si = RAG()
            k = map_coefficient_to_rag_k(self.energy)

            y = Si(collection=self.namespace, 
                k_value=k,
                hallucinate=False,
                document=self.mass_energy)


            return y


        elif self.domain == 'F' and 'op1' not in kwargs.keys(): 
            
            identity, prompt = db.fi()
            prompt = prompt.format(important_data=self.mass_energy)


            if self.runners_map['F'].upper() == 'LLAMA8B':

                ctx_size = (self.energy)
                Fi = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)



            else:

                raise ValueError('Wrong runner.')


            y = Fi(identity, prompt)

            return y


        elif self.domain == 'T' and 'op1' not in kwargs.keys(): 
            
            identity, prompt = db.ti()
            prompt = prompt.format(rational_data=self.mass_energy)


            if self.runners_map['T'].upper() == 'LLAMA8B':

                ctx_size = (self.energy)
                Te = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)

            else:

                raise ValueError('Wrong runner.')


            y = Te(identity, prompt)


            return y
        
                    
        elif self.domain == '2':

            identity, prompt = db.two()
            if self.runners_map['2'].upper() == 'LLAMA8B':

                ctx_size = (self.energy)
                ex = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)

            else:

                raise ValueError('Wrong runner.')



            x = kwargs['x']

            prompt = prompt.format(environment_data=x)
                
            y = ex(identity, prompt)

            return y


        elif self.domain == '5':

            identity, prompt = db.five()
            if self.runners_map['5'].upper() == 'LLAMA8B':

                ctx_size = (self.energy)
                ex = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)

            else:

                raise ValueError('Wrong runner.')

            x = kwargs['x']

            prompt = prompt.format(environment_data=x)

            y = ex(identity, prompt)

            return y


        elif self.domain == '8':


            identity, prompt = db.eight()
            if self.runners_map['8'].upper() == 'LLAMA8B':

                ctx_size = (self.energy)
                ex = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)
            else:

                raise ValueError('Wrong runner.')   
         

            x = kwargs['x']

            prompt = prompt.format(environment_data=x)

            y = ex(identity, prompt)

            return y


        elif self.domain == '11':


            identity, prompt = db.eleven()
            if self.runners_map['11'].upper() == 'LLAMA8B':

                ctx_size = (self.energy)  
                ex = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)
         
            else:

                raise ValueError('Wrong runner.')

            x = kwargs['x']

            prompt = prompt.format(environment_data=x)

            y = ex(identity, prompt)

            return y


        
        elif 'operator' in kwargs.keys():

            op = kwargs['operator'] 

            if op == '~': 

                if self.runners_map['JOINT'] == 'LLAMA8B':

                    ctx_size = (self.energy)
                    Joint = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)


                if self.symbol == 'Ti':

                    identity, prompt = db.ti()
                    prompt = prompt.format(logical_data=self.mass_energy)

                    if self.runners_map['T'].upper() == 'LLAMA8B':

                        n_ctx_size = (self.potential)
                        Ti = TextRunner(local=self.local, ctx_size=n_ctx_size, **self.runners_map)
                       
                    else:

                        raise ValueError('Wrong runner.')


                    Ti_sink = Ti(identity, prompt)

                    if x.symbol == 'Se':

                        Se_source = x
                        identity, prompt = db.ti_se_orbital()
                        prompt.format(logical_data = Ti_sink, environment_data = Se_source, memories = Se_source)
 
                        y = Joint(identity, prompt)

                        return y
                    
                    elif x.symbol == 'Si':

                        Si_sink = x
                        identity, prompt = db.ti_si_orbital()
                        prompt.format(logical_data = Ti_sink, memories = Si_sink)

                        y = Joint(identity, prompt)

                        return y
                    
                    elif x.symbol == 'Ne':

                        Ne_source  = x
                        identity, prompt = db.ti_ne_orbital()
                        prompt.format(logical_data = Ti_sink, environment_data = Ne_source)

                        y = Joint(identity, prompt)

                        return y
                    
                    elif x.symbol == 'Ni':


                        try:

                            Ni_sink = mpimg.imread(x) 
                            Ni_sink.save('Ni_sink.png')
                            identity, prompt = db.ni()
                            runner = LlavaRunner()
                            Ni_sink =runner(prompt=identity, image_path='Ni_sink.png', ctx_size=ctx_size)

                        except:

                            Ni_sink = x


                        identity, prompt = db.ti_ni_orbital()
                        prompt.format(logical_data = Ti_sink, narratives = Ni_sink)

                        y = Joint(identity, prompt)

                        return y
                    
                    else:

                        raise ValueError('Incorrect operands for orbital ~')


                elif self.symbol == 'Fi':

                    identity, prompt = db.fi()
                    prompt = prompt.format(important_data=self.mass_energy)

                    if self.runners_map['F'].upper() == 'LLAMA8B':

                        ctx_size = (self.potential)
                        Fi = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map) 
                    


                    else:

                        raise ValueError('Wrong runner.')



                    Fi_sink = Fi(identity, prompt)

                    if x.symbol == 'Se':

                        Se_source = x
                        identity, prompt = db.fi_se_orbital()
                        prompt.format(important_data = Fi_sink, environment_data = Se_source)

                        y = Joint(identity, prompt)

                        return y
                    

                    elif x.symbol == 'Si':

                        Si_sink = x
                        identity, prompt = db.fi_si_orbital()
                        prompt.format(important_data = Fi_sink, memories = Si_sink)

                        y = Joint(identity, prompt)

                        return y
                    
                    elif x.symbol == 'Ne':

                        Ne_source  = x
                        identity, prompt = db.fi_ne_orbital()
                        prompt.format(important_data = Fi_sink, environment_data = Ne_source)

                        y = Joint(identity, prompt)

                        return y
                    
                    elif x.symbol == 'Ni':

                        Ni_sink = x
                        identity, prompt = db.fi_ni_orbital()
                        prompt.format(important_data = Fi_sink, narratives = Ni_sink)

                        y = Joint(identity, prompt)

                        return y

                    else:

                        raise ValueError('Incorrect operands for orbital ~')


                elif self.symbol == 'Ni':


                    identity, prompt = db.ni()
                    prompt = prompt.format(narratives=self.mass_energy)

                    try:

                        Ni_sink = mpimg.imread(self.mass_energy) 
                        Ni_sink.save('Ni_sink.png')
                        identity, prompt = db.ni()
                        runner = LlavaRunner()
                        Ni_sink =runner(prompt=identity, image_path='Ni_sink.png', ctx_size=ctx_size)

                    except Exception:

                        Ni_sink = self.mass_energy



                    if self.runners_map['N'].upper() == 'LLAMA8B':

                        ctx_size = (self.potential)
                        Ni = TextRunner(local=self.local, ctx_size=ctx_size)
                    

                    else:

                        raise ValueError('Wrong runner.')


                    Ni_sink = Ni(identity, prompt)

                    if x.symbol == 'Fi':

                        Fi_sink = x
                        identity, prompt = db.ni_fi_orbital()
                        prompt.format(narratives = Ni_sink, important_data = Fi_sink)

                        y = Joint(identity, prompt)

                        return y
                    
                    elif x.symbol == 'Fe':

                        Fe_source  = x
                        identity, prompt = db.ni_fe_orbital()
                        prompt.format(narratives = Ni_sink, important_data = Fe_source)

                        y = Joint(identity, prompt)

                        return y


                    elif x.symbol == 'Te':

                        Te_source  = x
                        identity, prompt = db.ni_te_orbital()
                        prompt.format(narratives = Ni_sink, narrative_data = Te_source)

                        y = Joint(identity, prompt)

                        return y
                    
                    elif x.symbol == 'Ti':

                        Ti_sink = x
                        identity, prompt = db.ni_ti_orbital()
                        prompt.format(narratives = Ni_sink, logical_data = Ti_sink)

                        y = Joint(identity, prompt)

                        return y

                    else:

                        raise ValueError('Incorrect operands for orbital ~')


            elif op == 'oo':

                if self.runners_map['JOINT'].upper() == 'LLAMA8B':

                    ctx_size = (self.potential)
                    Joint = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)


                else:

                    raise ValueError('Wrong runner.')
                
                if self.symbol == 'Ti':

                    identity, prompt = db.ti_te_cardinal()
                    prompt.format(logical_data=self.mass_energy)

                    if self.runners_map['T'].upper() == 'LLAMA8B':

                        ctx_size = (self.potential)
                        Ti = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)


           
                    else:

                        raise ValueError('Wrong runner.') 


                    Ti_sink = Ti(identity, prompt)

                    Te_source = x
                    identity, prompt = db.ti_te_cardinal()
                    prompt.format(logical_data = Ti_sink, rational_data = Te_source)

                    y = Joint(identity, prompt)

                    return y
                    

                elif self.symbol == 'Fi':

                    identity, prompt = db.fi()
                    prompt = prompt.format(important_data=self.mass_energy)


                    if self.runners_map['F'].upper() == 'LLAMA8B':

                        ctx_size = (self.potential)
                        Fi = TextRunner(local=self.local, ctx_size=ctx_size)


                    else:

                        raise ValueError('Wrong runner.')


                    Fi_sink = Fi(identity, prompt)

                    Fe_source = x
                    identity, prompt = db.fi_fe_cardinal()
                    prompt.format(important_data = Fi_sink, external_important_things = Fe_source)

                    y = Joint(identity, prompt)
                   

                    return y
                

                elif self.symbol == 'Si':


                    k = map_coefficient_to_rag_k(self.potential)
                    Si = RAG(collection=self.namespace, 
                        k_value=k,
                        hallucinate=False,
                        document=self.mass_energy)
                    
                    Si_sink = Si(self.mass_energy)
                    Se_source = x
                    identity, prompt = db.si_se_cardinal()
                    prompt.format(memories = Si_sink, environment_data = Se_source)
                    ctx_size = (self.potential)
                    y = Joint(identity, prompt)

                    return y
                

                elif self.symbol == 'Ni':

                    try:

                        Ni_sink = mpimg.imread(self.mass_energy) 
                        Ni_sink.save('Ni_sink.png')
                        identity, prompt = db.ni()
                        runner = LlavaRunner()
                        Ni_sink =runner(prompt=identity, image_path='Ni_sink.png', ctx_size=ctx_size)

                    except Exception:

                        Ni_sink = self.mass_energy


                    if self.runners_map['N'].upper() == 'LLAMA8B':

                        ctx_size = (self.potential)
                        Ni = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)

                    else:

                        raise ValueError('Wrong runner.')

                    Ni_sink = Ni(identity, prompt)

                    Ne_source = x
                    identity, prompt = db.ni_ne_cardinal()
                    prompt.format(narratives = Ni_sink, environment_data = Ne_source)

                    y = Joint(identity, prompt)

                    return y


            elif op == '->':


                if self.runners_map['JOINT'].upper() == 'LLAMA8B':


                    ctx_size = (self.energy)
                    Joint = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)


                else:

                    raise ValueError('Wrong runner.')

                
                if self.symbol == 'Fi':

                    identity, prompt = db.fi()
                    prompt = prompt.format(important_data=self.mass_energy)

                    if self.runners_map['F'].upper() == 'LLAMA8B':

                        ctx_size = (self.potential)
                        Fi = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)
                    
      
                    else:

                        raise ValueError('Wrong runner.')

                      
                    Fi_sink = Fi(identity, prompt)

                    Te_source = x
                    identity, prompt = db.fi_te_fixed()
                    prompt.format(important_data = Fi_sink, rational_data = Te_source)

                    y = Joint(identity, prompt)

                    return y
                
                elif self.symbol == 'Si':

                    k = map_coefficient_to_rag_k(self.potential)
                    Si = RAG(collection=self.namespace, 
                        k_value=k,
                        hallucinate=False,
                        document=self.mass_energy)
                    
                    Si_sink = Si(self.mass_energy)
                    Ne_source = x
                    identity, prompt = db.si_ne_fixed()
                    prompt.format(memories = Si_sink, environment_data = Ne_source)
                    ctx_size = (self.potential)
                    y = Joint(identity, prompt)

                    return y
                
                elif self.symbol == 'Ni':

                    try:

                        Ni_sink = mpimg.imread(self.mass_energy) 
                        Ni_sink.save('Ni_sink.png')
                        identity, prompt = db.ni()
                        runner = LlavaRunner()
                        Ni_sink =runner(prompt=identity, image_path='Ni_sink.png', ctx_size=ctx_size)

                    except Exception:

                        Ni_sink = self.mass_energy


                    if self.runners_map['N'].upper() == 'LLAMA8B':

                        ctx_size = (self.potential)
                        Ni = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)

                    else:

                        raise ValueError('Wrong runner.')


                    Ni_sink = Ni(identity, prompt)

                    Se_source = x
                    identity, prompt = db.ni_se_fixed()
                    prompt.format(narratives = Ni_sink, environment_data = Se_source)

                    y = Joint(identity, prompt)

                    return y


                elif self.symbol == 'Ti':

                    identity, prompt = db.ti()
                    prompt = prompt.format(logical_statements=self.mass_energy)

                    if self.runners_map['T'].upper() == 'LLAMA8B':

                        ctx_size = (self.potential)
                        Ti = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)

                    else:

                        raise ValueError('Wrong runner.')

                    Ti_sink = Ti(identity, prompt)


                    Fe_source = x
                    identity, prompt = db.ti_fe_fixed()
                    prompt.format(logical_statements = Ti_sink, environment_data = Fe_source)

                    y = Joint(identity, prompt)

                    return y


                else:

                    raise ValueError('Wrong operands on op ->')
                


        else:

            raise ValueError('Domain must be N, S, F, or T')






class Proportional:



    def __init__(self, domain, energy, potential, runners_map) -> None:
        """
        Initializes a new instance of the class with the given domain, energy, and potential.

        Args:
            domain (str): The domain of the object.
            energy (float): The energy of the object.
            potential (float): The potential of the object.

        Returns:
            None
        """

        self.domain = domain.upper()
        self.energy = energy
        self.potential = potential
        self.runners_map = runners_map


    def __call__(self, **kwargs):

        x1 = kwargs['x1']
        x2 = kwargs['x2']

       
        if self.runners_map['JOINT'].upper() == 'LLAMA8B':

            ctx_size = (self.potential)
            Joint = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)

        else:

            raise ValueError('Wrong runner.')


        if self.domain == 'NS':


            identity, prompt = db.ns()
            prompt.format(data_about_the_future = x1, data_about_the_present = x2)

            y = Joint(identity, prompt)

            return y


        elif self.domain == 'SN':

            identity, prompt = db.sn()
            prompt.format(data_about_the_present = x1, data_about_the_future = x2)

            y = Joint(identity, prompt)

            return y
            
        elif self.domain == 'TF':

            identity, prompt = db.tf()
            prompt.format(logical_statements= x1, emotional_statements = x2)

            y = Joint(identity, prompt)

            return y

        elif self.domain == 'FT':

            identity, prompt = db.ft()
            prompt.format(emotional_statements = x1, logical_statements = x2)

            y = Joint(identity, prompt)

            return y


        elif self.domain == '3':
            
            identity, prompt = db.three()

            if self.runners_map['3'].upper() == 'LLAMA8B':

                ctx_size = (self.energy)
                ex = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)
            else:

                raise ValueError('Wrong runner.')
 

            x = kwargs['x']

            prompt = prompt.format(environment_data=x)

            y = ex(identity, prompt)

            return y
 

        elif self.domain == '6':

            identity, prompt = db.six()

            if self.runners_map['6'].upper() == 'LLAMA8B':

                ctx_size = (self.energy)
                ex = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)

            else:

                raise ValueError('Wrong runner.')
    

            x = kwargs['x']

            prompt = prompt.format(environment_data=x)

            y = ex(identity, prompt)

            return y


        elif self.domain == '9':

            identity, prompt = db.nine()

            
            if self.runners_map['9'].upper() == 'LLAMA8B':

                ctx_size = (self.energy)
                ex = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)

          
            else:

                raise ValueError('Wrong runner.')
    

            x = kwargs['x']

            prompt = prompt.format(environment_data=x)

            y = ex(identity, prompt)

            return y
 
 
        elif self.domain == '12':


            identity, prompt = db.twelve()

            if self.runners_map['12'].upper() == 'LLAMA8B':

                ctx_size = (self.energy)
                ex = TextRunner(local=self.local, ctx_size=ctx_size, **self.runners_map)
            else:

                raise ValueError('Wrong runner.')

            x = kwargs['x']

            prompt = prompt.format(environment_data=x)

            y = ex(identity, prompt)

            return y

      
 
        else:

            raise ValueError('Wrong parameters')




class AngularMomentumMapper:




    def conjugation(self, a, b):
        
        identity = """

            You are a narrator describing a story between two people (A an B) who are equal to each other. Because they are similar, they add-up the same amount of energy.

        """

        prompt = f"""

        Life so far of person A

           {a} 

        Life so far of person B:

            {b}

        """

        return identity, prompt


    
    def opposition(self, a, b):
                
        identity = """

            You are a narrator describing a story between two people (A an B) who are opposite to each other. Because they are opposite, they are at tension and the strongest person helps the weaker person. 

        """

        prompt = f"""

        Life so far of person A

           {a} 

        Life so far of person B:

            {b}

        """

        return identity, prompt



   
    def trine(self, a, b):
        
                
        identity = """

            You are a narrator describing a story between two people (A an B) who are similar in characteristics to each other. Because they are similar, they feed upon each other to create a magnified flowing summation of both stories.

        """

        prompt = f"""

        Life so far of person A

           {a} 

        Life so far of person B:

            {b}

        """

        return identity, prompt
  
    def square(self, a, b):
        
        identity = """

            You are a narrator describing a story between two people who are different and incongruent to each other. Because they are different, theres tension between them.

        """

        prompt = f"""

        Life so far of person A

           {a} 

        Life so far of person B:

            {b}

        """

        return identity, prompt


    def sextile(self, a, b):

        identity = """

            You are a narrator describing a story between two people who are different but kindred to each other. Because they are kindred their story comes up together mixed. 

        """

        prompt = f"""

        Life so far of person A

           {a} 

        Life so far of person B:

            {b}

        """

        return identity, prompt





    def inconjunct(self, a, b):
        identity = """

            You are a narrator describing a story between two people who are different but kindred to each other. Because they are kindred their story comes up together mixed. 

        """

        prompt = f"""

        Life so far of person A

           {a} 

        Life so far of person B:

            {b}

        """

        return identity, prompt



    def semi_sextile(self, a, b):
        identity = """

            You are a narrator describing a story between two people who are uneven. One recognizes the past in person A, and person A recognizes a future in person B. 

        """

        prompt = f"""

        Life so far of person A

           {a} 

        Life so far of person B:

            {b}

        """

        return identity, prompt



  



class CharacterOperationMapper:



    def duality(a, b):

        identity = """


            You are a narrator describing a story between two people who are opposite but desiring each other. One recognizes the future in person A, and person A recognizes a future in person B. 

        """

        prompt = f"""

        Life so far of person A:

           {a} 

        Life so far of person B:

            {b}

        """

        return identity, prompt



    def identical(self, a ,b):
        
        identity = """


            You are a narrator describing a story between two people who are exactly the same to each other.
        """

        prompt = f"""

        Life so far of person A:

           {a} 

        Life so far of person B:

            {b}

        """

        return identity, prompt



    def activity(self, a, b):
                
        identity = """

            You are a narrator describing a story between two people who are pleasent to each while performing an activity where both are proficient at but have trouble communicating outside the context of such activity. 
        """

        prompt = f"""

        Life so far of person A:

           {a} 

        Life so far of person B:

            {b}

        """

        return identity, prompt


    def mirror(self, a, b):
        
        identity = """

            You are a narrator describing a story between two people who are mirrors to each other. Every partnet have similar interests and ideas, but a slightly different understanding of the same problems. Each partner can see only half of one problem. Therefore the partners always find what the other partner is thinking interesting. Usually partners quickly realise that they are very like-minded.    """

        prompt = f"""

        Life so far of person A:

           {a} 

        Life so far of person B:

            {b}

        """

        return identity, prompt



    def superego(self, a, b):

        identity = """

            You are a narrator describing a story between two people who are distant and slightly mysterious ideal. 
            
            
            They often show interest in each other's manners, behaviour and thought composition. Both partners experience a warm feeling towards each other, but for the outsider, these relations may look cold.
            
             
        """

        prompt = f"""

        Life so far of person A:

           {a} 

        Life so far of person B:

            {b}

        """

        return identity, prompt



    def semi_duality(self, a, b):
        
        identity = """

            You are a narrator describing a story between two people who  have no problems in understanding each other or each other's objectives, at least when these objectives are only on paper. When it comes to fulfilling joint plans, partners often fail to co-operate. The extrovert partner hardly listens to the introvert, concentrating more on the sound of their own voice. However, the introvert partner does not get upset about this and they often seem to find a way to adapt to it. 
            
            Semi-Duals usually have many topics for conversation and these conversations do not seem to be boring.
             
        """

        prompt = f"""

        Life so far of person A:

           {a} 

        Life so far of person B:

            {b}

        """

        return identity, prompt


    def comparative(self, a, b):

        identity = """

            You are a narrator describing a story between two people who  have no problems in understanding each other or each other's objectives, at least when these objectives are only on paper. When it comes to fulfilling joint plans, partners often fail to co-operate. The extrovert partner hardly listens to the introvert, concentrating more on the sound of their own voice. However, the introvert partner does not get upset about this and they often seem to find a way to adapt to it. 
            
            Semi-Duals usually have many topics for conversation and these conversations do not seem to be boring.
             
        """

        prompt = f"""

        Life so far of person A:

           {a} 

        Life so far of person B:

            {b}

        """

        return identity, prompt



    def conflicting(self, a, b):

        identity = """

            You are a narrator describing a story between two people who show deceptive similarity. Comparative partners talk about similar things, have similar interests, obey the norms of politeness and hospitality towards each other but they never really show an interest in each others problems. After a while these relations can become boring and stagnant. When comparative partners are on the same level in a hierarchy, they can coexist quite peacefully. Once one partner becomes superior to the other, they may have serious disagreements and conflicts. 
        """

        prompt = f"""

        Life so far of person A:

           {a} 

        Life so far of person B:

            {b}

        """

        return identity, prompt



    def quasi_identical(self, a, b):
        identity = """

            You are a narrator describing a story between two people who  can interact with each other in a more or less peaceful manner if both partners are Thinking types. If they are both Feeling types however, they are likely to have an argumentative relationship. Also, as in the other relations, personal attraction can be very crucial to the peacefulness in their relationship. An absence of personal attraction may cause unnecessary internal tension resulting in conflict between partners. However these arguments do not often last long. After both partners have released their internal tension, the Perceiving partner is usually the first to show the initiative in reconciliation.

            A positive aspect of these relations is that Quasi-Identical partners do not underline your weak points and therefore are not viewed as dangerous by each other. Neither do they see each other as equal. Each partner sees the other as less capable than themselves, hence less talented. However, Quasi-Identicals mistakenly believe that their partner is achieving more than they are. This is perceived by both partners as injustice and may hinder the ambitions of both.

            In these relations partners always have difficulty understanding each other in full. Quasi-Identical partners always need to convert each other's information in such a way that it corresponds with their own understanding. This conversion requires much energy and does not bring the desired satisfaction.
                            
        """

        prompt = f"""

        Life so far of person A:

           {a} 

        Life so far of person B:

            {b}

        """

        return identity, prompt




    def contrary(self, a, b):

        identity = """

            You are a narrator describing a story between two people who unstable psychological distance. Both partners experience difficulties in establishing and keeping a stable psychological distance between them. The only chance Contrary partners have to get on together well with each other is if they are left alone. In other cases partners usually compete over their strong sides. The reason for this is when somebody else is present, each partner tries to capture the attention of the listener by showing off their strong side. Contrary partners may like some elements of the other partner's behaviour. This often helps the partners to begin a more close relationship.
                    
        """

        prompt = f"""

        Life so far of person A:

           {a} 

        Life so far of person B:

            {b}

        """

        return identity, prompt


    def illusionary(self, a, b):
        
        identity = """

            You are a narrator describing a story between two people who find it comfortable being relaxed together, discussing different subjects. What one partner is talking about is always interesting, but in order to understand the partner better the other partner needs to force themselves. This difficulty in making an effort also makes achieving goals together almost impossible.                     
        """

        prompt = f"""

        Life so far of person A:

           {a} 

        Life so far of person B:

            {b}

        """

        return identity, prompt

    def lookalike(self, a, b):
        identity = """

            You are a narrator describing a story between two people who can be called acquaintances rather than friends. There are no visual obstacles in the development of these relations, partners can talk easily almost about anything. Look-a-like partners do not feel any danger from the other partner. The strong sides of the partners are different in the such a way that almost any conversations between them always fall into the area of the confidence of only one of the partners. Look-a-like partners also have similar problems which makes them feel rather sympathetic towards each other instead of being critical of each other's vulnerabilities.
                     
        """

        prompt = f"""

        Life so far of person A:

           {a} 

        Life so far of person B:

            {b}

        """

        return identity, prompt



    def benefit(self, a, b):
        identity = """

            You are a narrator describing a story between two people who are asymmetrical. One partner A, called the Benefactor, is always in a more favourable position in respect to the other partner B who is known as Beneficiary.

            The Beneficiary thinks of the Benefactor as an interesting and meaningful person, usually over-evaluating them in the beginning. The Beneficiary can be impressed and delighted by their partner's behaviour, manners, thoughts and their ability to easily deal with things that the Beneficiary conceives as complicated. When partners are together, the Beneficiary involuntarily starts to ingratiate themselves with the Benefactor, trying to please them without any obvious reason. In the worst cases this starts from little things and then becomes bigger until the Beneficiary realises the foolishness of their situation. 

        """

        prompt = f"""

        Life so far of person A:

           {a} 

        Life so far of person B:

            {b}

        """

        return identity, prompt




    def supervision(self, a, b):
        identity = """

            You are a narrator describing a story between two people who are relations of Benefit. One partner A, called the Supervisor, is always in a more favourable position in respect to the other partner B who is known as Supervisee.

            Relations of Supervision can give the impression that Supervisor is constantly watching every step of the Supervisee. The latter usually feels this control even if the Supervisor does not say or do anything. The explanation for this is that the Supervisee weak point is defenceless against the Supervisor's strong point. This makes the Supervisee nervous and expect the worse.

            Although the Supervisor can seem self-satisfied, petty, faultfinding and narrative, the Supervisee pays attention to their actions and considers the Supervisor as consequential. The Supervisee normally wants to gain recognition and commendation from the Supervisor. However, it may seem like the Supervisor always undervalues the abilities of the Supervisee. This stimulates the Supervisee into proving their own worthiness with various actions, yet there is little chance that they will succeed.

            The Supervisor sees the Supervisee as quite interesting and capable, but incomplete and therefore in need of some help and advice. The Supervisee does not respond to this aid as expected and this will often increase the Supervisor's attempts to change the Supervisee. Because the Supervisee naturally does not understand what it is that the Supervisor wants from them, this may irritate the Supervisor, who thinks that the Supervisee simply does not want to understand.
    
        """

        prompt = f"""

        Life so far of person A:

           {a} 

        Life so far of person B:

            {b}

        """

        return identity, prompt



       



class HouseMapper:
 
    def one(self, environment_data):

        
        identity = """ 
        
        You are an cognitive agent. You judge things superficially. 
        
        Your aim is to destroy or change what is hindering you from accomplishing something.

        You hate rules and restrictions. Your wan't to win at all costs and satisfy your desires.

        """

        prompt = f"""
            Environment data:

                {environment_data}

            Answer:

        """
        return identity + prompt, "one"

    def two(self, environment_data):

        identity = """

            You are a cognitive agent. You wan't to accumulate posessions.

            Your aim is to improve your well being, and benefit yourself with things that promise pleasent experiences.

        """

        prompt = f"""
            Environment data:

                {environment_data}

            Answer:

        """

        return identity + prompt, "two"
        
    def three(self, environment_data):

        identity = """
            You are cognitive agent. You wan't to prove your wit; and find solutions to problems.

            You are regarded as an intelligent person. You value knowledge. Your aim is to communicate your logical thoughts on problems you have identified.

        """

        prompt = f"""
            Environment data:

                {environment_data}
            
            Answer:

        """

        return identity + prompt, "three"
    

    def four(self, environment_data):

        identity = """

            You are a cognitive agent. You cherish your memories, and you regard yourself as important as the things that have happened to you.

            Your aim is to take care of yourself and things or people you feel are important.
            
            You have a soft touch and are very self-protective.
        """

        prompt = f"""

            Environment data:  

                {environment_data}

            Answer:

        """

        return identity + prompt, "four"

    def five(self, environment_data):


        identity = """  

            You are a cognitive agent. You are opinionated and wan't to prove that you are the best you can be.

            You value the opinions of others when they acknowledge greatness in you. Your aim is to be remembered as an important person.

            You speak greatly and with esteem of things you find important.

        """

        prompt = f"""

            Environment data:

                {environment_data}
            
            Answer:

        """


        return identity + prompt, "five"


    def six(self, environment_data):


        identity = """

            You are a cognitive agent. You wan't to rememeber everyone of what is important. You are dutiful and detail oriented.

            Your aim is service, and make things as perfect as possible.

        """

        prompt = f"""

            Environment data:   

                {environment_data}

            Answer:

        """

        return  identity + prompt, "six"


    def seven(self, environment_data):

        identity = """
            You are a cognitive agent. You are very communicative and love knowing what other people are up to. 

            You are very social and take decisions on the basis of what other people think is important.

            Your aim is to achieve balance with other people.

        """

        prompt = f"""

            Environment data:   

                {environment_data}

            Answer:
        """

        return identity + prompt, "seven"


    def eight(self, environment_data):


        identity = """

            You are a cognitive agent. You are mysterious and intense. You are obsessive and private.

            Your aim is to transform yourself. You seek to achieve your goals at all costs.


        """

        prompt = f"""

            Environment data:   

                {environment_data} 

            Answer:

        """

        return identity + prompt , "eight"

    def nine(self, environment_data):


        identity = """
            You are a cognitive agent. You are curious and wise. You seek to find the meaning of things.

            Your aim is to find a purpose, you are a philosopher and adventurer who wants to explore the possibilities of things.

            You like movement because it helps you understand where things are destined to be.
        """

        prompt = f"""

            Environment data:   

                {environment_data}

            Answer:

        """

        return identity + prompt, "nine"

    def ten(self, environment_data):


        identity = """

            You are a cognitive agent. You are disciplined. You seek to achieve your objectives in a lawful and orderly manner.

            You are logical, and you excel at managing resources with logic and rationality. Your aim is to maximize your potential and sucesss.

        """

        prompt = f"""

            Environment data:   

                {environment_data}

            Answer:

        """


        return identity + prompt, "ten"
    
    def eleven(self, environment_data):

        identity = """

            You are a cognitive agent. You are humanitarian. You seek to bring progress and improve the life of other people.


            You are logical aswell as aware of what other people wan't. You excel at making everyone happy.

        """

        prompt = f"""

            Environment data:   

                {environment_data}

            Answer:

        """

        return identity + prompt, "eleven"

    def twelve(self, environment_data):


        identity = """

            You are a cognitive agent. You are fantasist aswell as a performer. You seek to imaginate the destinies of other people, to figure out a destiny for yourself.


            Your aim is defend your beliefs and perform whats important. You weight many possibilities and decide on one to perform.

        """

        prompt = f"""

            Environment data:   

                {environment_data}

            Answer:

        """

        return identity + prompt, "twelve"


class Map:




    def __init__(self, runners_map) -> None:
        
        """
        Initializes an instance of the Reducers class with the given parameters.

        Args:
            runners_map (dict[str, Callable[[str, str], str]]): A dictionary
                mapping technique names to their corresponding runner functions.

        Returns:
            None
        """
        self.runners_map = runners_map


    def densifier(self, chunks):
        
        """
        Returns a tuple containing an identity string and a prompt string.
        The identity string is a creative writing prompt that asks the user to
        find a pattern and come up with a list of references in both music and
        movie scenes based on the given chunks of text.
        The prompt string is a string that describes the chunks of text
        and asks the user to find a pattern and come up with a list of references
        in both music and movie scenes based on them.

        Parameters
        ----------

        chunks : str
            A string describing the chunks of text.

        Returns
        -------

        tuple
            A tuple containing the identity string and the prompt string.
        """
        identity = """"
            You are an expert in both music and contemporary culture seeking to 'put the points together'. 
            
            You seek to create a metaverse or multi-universe where things are interconnected by gestalts and common patterns.
         
        """
        prompt = f"""

            Find patterns and come up a list of references in both music and movie scenes based on the following documents:

                {chunks} 

        """

        return identity, prompt



    def paraphraser(self, theme, event):
        
        """
        Returns a tuple containing the theme and a prompt string.
        The prompt string is a string that asks the user to paraphrase
        and romanticize the given event using the given theme.

        Parameters
        ----------

        theme : str
            The theme to use for paraphrasing and romanticizing the event.

        event : str
            The event to paraphrase and romanticize.

        Returns
        -------

        tuple
            A tuple containing the theme and the prompt string.
        """
        prompt = f"""

            Paraphrase rewrite and romaticize the following event using the theme '{theme}':


                {event}


        """ 

        return theme, prompt


    def record(self, scene, ambiance):

        """
        Returns an image that represents the given scene and ambiance.

        Parameters
        ----------

        scene : str
            A string describing the scene.

        ambiance : str
            A string describing the ambiance of the scene.

        Returns
        -------
        image
            An image that represents the given scene and ambiance.
        """
        image_builder = FluxRunner()
        image = image_builder(scene + ' ' + ambiance)

        return image


    def iconize(self, technique, power_mode): 

        """
        Returns an image that represents the given technique.

        Parameters
        ----------

        technique : str
            A string describing the technique.

        power_mode : str
            A string describing the power mode. Must be one of 'low_power', 'medium_power', or 'high_power'.

        Returns
        -------
        image
            An image that represents the given technique.
        """
        if power_mode == 'low_power':

            image_builder = ImageRunner(low_power=True)
        
        elif power_mode == 'medium_power':

            image_builder = ImageRunner(low_power=False)

        elif power_mode == 'high_power':

            image_builder = SDXLRunner()
        
        else:

            raise ValueError('Invalid power mode')

        image = image_builder('emblem of ' + technique + ' very detailed, high contrast, intricate lines.')

        return image



    def entities(self, document, n_entities):
        """
        Extracts entities from the given document using the given entity extraction runner.

        Parameters:
            document (str): The text document to extract entities from.
            n_entities (int): The number of entities to extract.

        Returns:
            list[str]: A list of entities extracted from the document.
        """
        runner = self.runners_map['entity_extraction']

        sys = """
            You find entities in the following text.
        """

        prompt =f"""
            Extract the {n_entities} ammount of  entities from the following text:

            {document}

        """

        entities = runner(sys, prompt)

        return entities
    


    def text_fision(self, document, ensemble_size):
        """
        Generates an ensemble of text techniques using Orb, House and Piece
        reducers. The ensemble is composed of the highest ranked techniques
        from each reducer.

        Parameters:
         
            document (str): The text document to analyze.
            ensemble_size (int): The number of techniques to include in the
                ensemble.

        Returns:
            Ensemble: An Ensemble object containing the highest ranked
                techniques from each reducer, along with their corresponding
                scores.
        """
        expert = self.runners_map['high']
    
        sys = """

            You re a literature coinosseur with an interest in psychology.
        
        """

        prompt = f"""

            Analyze the following document and provide extensive detailed insight about it juxtaposing it with many references.

                {document} 

        """


        analysis = expert(sys, prompt) 

        orb_filter = (
            OrbFilter.one,  OrbFilter.eleven, OrbFilter.twentythree,
            OrbFilter.two,  OrbFilter.twelve, OrbFilter.twentyfour,
            OrbFilter.three,OrbFilter.fourteen, OrbFilter.twentyfive,
            OrbFilter.four, OrbFilter.fifteen, OrbFilter.twentysix,
            OrbFilter.five, OrbFilter.sixteen, OrbFilter.twentyseven,
            OrbFilter.six,  OrbFilter.seventeen, OrbFilter.twentyeight,
            OrbFilter.seven,OrbFilter.nineteen, OrbFilter.twentynine,
            OrbFilter.eight,OrbFilter.twenty,   OrbFilter.thirteen,
            OrbFilter.nine, OrbFilter.twentyone, OrbFilter.thirteenone,
            OrbFilter.tenth,OrbFilter.twentytwo, OrbFilter.thirteentwo,
    OrbFilter.thritythree, OrbFilter.thirtyfour, OrbFilter.thirtyfive, OrbFilter.thirtysix
        )


        house_filter = (HouseFilter.one, HouseFilter.two, HouseFilter.three, 
                        HouseFilter.four, HouseFilter.five, HouseFilter.six, 
                        HouseFilter.seven, HouseFilter.eight, HouseFilter.nine, 
                        HouseFilter.ten, HouseFilter.eleven, HouseFilter.twelve)


        piece_filter = (PieceFilter.one, PieceFilter.two, PieceFilter.three, 
                        PieceFilter.four, PieceFilter.five, PieceFilter.six,
                        PieceFilter.seven, PieceFilter.eight, PieceFilter.nine, 
                        PieceFilter.ten, PieceFilter.eleven, PieceFilter.twelve)



        runner = self.runners_map['low']

        orb_convolutions = [ {idx:runner(orb.format(document=analysis)) }for idx, orb in enumerate(orb_filter)]
        highest_orb_spectrum = list(sorted(orb_convolutions))[:ensemble_size]

        house_convolutions = [ {idx: runner(house.format(document=analysis))} for house in enumerate(house_filter)]
        highest_house_spectrum = list(sorted(house_convolutions))[:ensemble_size]  

        piece_convolutions = [ { piece.__name__: runner(piece.format(document=analysis))} for piece in piece_filter]
        highest_piece_spectrum = list(sorted(piece_convolutions))[:ensemble_size]
        fusion = Reduce().fusion
        
        basis_collection = []
        position_collections = []
        superposition_collections = []

        idx = 0

        for  element in zip(highest_orb_spectrum, highest_house_spectrum, highest_piece_spectrum):

            if element[0]['dim'] == 2:

                basis_collection.append(
                    fusion(
                        formula=element[0]['formula'] ,
                        acceleration=element[0]['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        runners_map=self.runners_map
                    )
                )


                position_collections.append(
                    fusion(
                        formula=element[0]['formula'] ,
                        acceleration=element[0]['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        runners_map=self.runners_map
                    )
                )

                superposition_collections.append(
                    fusion(
                        formula=element[0]['formula'] ,
                        acceleration=element[0]['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        runners_map=self.runners_map
                    )
                )
            
            elif element[0]['dim'] == 3:


                third_mass =  "Original Document:\n" + document + "\nExpert Anlysis:\n" + analysis


                basis_collection.append(
                            fusion(
                                formula=element[0]['formula'] ,
                                acceleration=element[0]['acceleration'],
                                me_1=document,
                                me_2=analysis,
                                me_3 = third_mass,
                                runners_map=self.runners_map
                            )
                        )


                position_collections.append(
                    fusion(
                        formula=element[0]['formula'] ,
                        acceleration=element[0]['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        me_3 = third_mass,
                        runners_map=self.runners_map
                    )
                )

                superposition_collections.append(
                    fusion(
                        formula=element[0]['formula'] ,
                        acceleration=element[0]['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        me_3 = third_mass,
                        runners_map= self.runners_map
                    )
                )


            elif element[0]['dim'] == 4:
                    
                    third_mass = "Original Document:\n" + document + "\nExpert Anlysis:\n" + analysis
                    fourht_mass = document

                    basis_collection.append(
                            fusion(
                                formula=element[1]['formula'] ,
                                acceleration=element[1]['acceleration'],
                                me_1=document,
                                me_2=analysis,
                                me_3 = third_mass,
                                me_4 = fourht_mass,
                                runners_map=self.runners_map
                            )
                        )


                    position_collections.append(
                        fusion(
                            formula=element[1]['formula'] ,
                            acceleration=element[1]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            me_4 = fourht_mass,
                            runners_map=self.runners_map
                        )
                    )

                    superposition_collections.append(
                        fusion(
                            formula=element[1]['formula'] ,
                            acceleration=element[1]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            me_4 = fourht_mass,
                            runners_map= self.runners_map
                        )
                    )


            elif element[1]['dim'] == 2:

                basis_collection.append(
                    fusion(
                        formula=element[1]['formula'] ,
                        acceleration=element[1]['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        runners_map=self.runners_map
                    )
                )


                position_collections.append(
                    fusion(
                        formula=element[1]['formula'] ,
                        acceleration=element[1]['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        runners_map=self.runners_map
                    )
                )

                superposition_collections.append(
                    fusion(
                        formula=element[1]['formula'] ,
                        acceleration=element[1] ['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        runners_map=self.runners_map
                    )
                )
            
            elif element[1]['dim'] == 3:


                third_mass =  "Original Document:\n" + document + "\nExpert Analysis:\n" + analysis


                basis_collection.append(
                            fusion(
                                formula=element[1]['formula'] ,
                                acceleration=element[1]['acceleration'],
                                me_1=document,
                                me_2=analysis,
                                me_3 = third_mass,
                                runners_map=self.runners_map
                            )
                        )


                position_collections.append(
                    fusion(
                        formula=element[1]['formula'] ,
                        acceleration=element[1]['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        me_3 = third_mass,
                        runners_map=self.runners_map
                    )
                )

                superposition_collections.append(
                    fusion(
                        formula=element[1]['formula'] ,
                        acceleration=element[1]['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        me_3 = third_mass,
                        runners_map= self.runners_map
                    )
                )


            elif element[2]['dim'] == 2:
                    
                    third_mass = "Original Document:\n" + document + "\nExpert Analysis:\n" + analysis
                    fourht_mass = document  

                    basis_collection.append(
                            fusion(
                                formula=element[2]['formula'] ,
                                acceleration=element[2]['acceleration'],
                                me_1=document,
                                me_2=analysis,
                                me_3 = third_mass,
                                me_4 = fourht_mass,
                                runners_map=self.runners_map
                            )
                        )


                    position_collections.append(
                        fusion(
                            formula=element[2]['formula'] ,
                            acceleration=element[2]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            me_4 = fourht_mass,
                            runners_map=self.runners_map
                        )
                    )

                    superposition_collections.append(
                        fusion(
                            formula=element[2]['formula'] ,
                            acceleration=element[2]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            me_4 = fourht_mass,
                            runners_map= self.runners_map
                        )
                    )
           


            elif element[2]['dim'] == 3:
                    
                    third_mass = "Original Document:\n" + document + "\nExpert Analysis:\n" + analysis
                    fourht_mass = document  

                    basis_collection.append(
                            fusion(
                                formula=element[2]['formula'] ,
                                acceleration=element[2]['acceleration'],
                                me_1=document,
                                me_2=analysis,
                                me_3 = third_mass,
                                me_4 = fourht_mass,
                                runners_map=self.runners_map
                            )
                        )


                    position_collections.append(
                        fusion(
                            formula=element[2]['formula'] ,
                            acceleration=element[2]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            me_4 = fourht_mass,
                            runners_map=self.runners_map
                        )
                    )

                    superposition_collections.append(
                        fusion(
                            formula=element[2]['formula'] ,
                            acceleration=element[2]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            me_4 = fourht_mass,
                            runners_map= self.runners_map
                        )
                    )
           
            elif element[2]['dim'] == 4:
                    
                    third_mass = "Original Document:\n" + document + "\nExpert Anlysis:\n" + analysis
                    fourht_mass = document  

                    basis_collection.append(
                            fusion(
                                formula=element[2]['formula'] ,
                                acceleration=element[2]['acceleration'],
                                me_1=document,
                                me_2=analysis,
                                me_3 = third_mass,
                                me_4 = fourht_mass,
                                runners_map=self.runners_map
                            )
                        )


                    position_collections.append(
                        fusion(
                            formula=element[2]['formula'] ,
                            acceleration=element[2]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            me_4 = fourht_mass,
                            runners_map=self.runners_map
                        )
                    )

                    superposition_collections.append(
                        fusion(
                            formula=element[2]['formula'] ,
                            acceleration=element[2]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            me_4 = fourht_mass,
                            runners_map= self.runners_map
                        )
                    )
            
                    
        ambiance = Ensemble(

            basis= basis_collection,
            position = position_collections,
            superposition = superposition_collections
        )
        

        identity = """

            You are a detective expert in analzying situations and people traits. You describe people perfectly and with great detail.

        """

        prompt = """

            Analyze with great detail the people or character of the following document: what are they wearing? what their face looks like? what impression do they give?. Answer with N/A if the image features no people.

             {document}
        """ 

        character = runner(identity, prompt)

        if len(character) > 50:

            character_filter = (
                CharacterFilter.one, CharacterFilter.two, CharacterFilter.three, CharacterFilter.four,
                CharacterFilter.five, CharacterFilter.six, CharacterFilter.seven, CharacterFilter.eight,
                CharacterFilter.nine, CharacterFilter.ten, CharacterFilter.eleven, CharacterFilter.twelve)

            highest_mbti_character = [ {character.__name__:runner(identity, prompt)}for character in character_filter][:4]


            house_filter = (
                HouseFilter.one, HouseFilter.two, HouseFilter.three, HouseFilter.four,
                HouseFilter.five, HouseFilter.six, HouseFilter.seven, HouseFilter.eight,
                HouseFilter.nine, HouseFilter.ten, HouseFilter.eleven, HouseFilter.twelve)
            
            highest_house = [ {house.__name__:runner(identity, prompt)}for house in house_filter][:1]


            return ambiance, highest_mbti_character, highest_house 
        
        else:

            return ambiance




    def image_fision(self, image, ensemble_size):
        """
        Generates an ensemble of image techniques using Orb, House and Piece
        reducers. The ensemble is composed of the highest ranked techniques
        from each reducer.

        Parameters:
            expert (Callable[[str, str], str]): A function that takes a system
                prompt and a user prompt and returns an expert response.
            runners_map (dict[str, Callable[[str, str], str]]): A dictionary
                mapping technique names to their corresponding runner functions.
            document (str): The text document to analyze.
            ensemble_size (int): The number of techniques to include in the
                ensemble.

        Returns:
            Ensemble: An Ensemble object containing the highest ranked
                techniques from each reducer, along with their corresponding
                scores.
        """
        runner = self.runners_map['image']

        identity = """

            You describe images. 

        """

        prompt = """
            Describe the following image:

        """


        document = runner(identity, prompt, image)


        runner = self.runners_map['image']

        identity = """

            You are an art coinnosseur. You analyze the ambience of images and visual media.

        """

        prompt = """
            Analyze with great detail the ambience of the following image:

        """


        analysis = runner(identity, prompt, image)


    
        orb_filter = (
            OrbFilter.one, OrbFilter.eleven, OrbFilter.twentythree,
            OrbFilter.two, OrbFilter.twelve, OrbFilter.twentyfour,
            OrbFilter.three, OrbFilter.fourteen, OrbFilter.twentyfive,
            OrbFilter.four, OrbFilter.fifteen, OrbFilter.twentysix,
            OrbFilter.five, OrbFilter.sixteen, OrbFilter.twentyseven,
            OrbFilter.six, OrbFilter.seventeen, OrbFilter.twentyeight,
            OrbFilter.seven, OrbFilter.nineteen, OrbFilter.twentynine,
            OrbFilter.eight, OrbFilter.twenty, OrbFilter.thirteen,
            OrbFilter.nine, OrbFilter.twentyone, OrbFilter.thirteenone,
            OrbFilter.tenth, OrbFilter.twentytwo, OrbFilter.thirteentwo,
             OrbFilter.thritythree, OrbFilter.thirtyfour, OrbFilter.thirtyfive,
             OrbFilter.thirtysix
        )


        house_filter = (HouseFilter.one, HouseFilter.two, HouseFilter.three, 
                        HouseFilter.four, HouseFilter.five, HouseFilter.six, 
                        HouseFilter.seven, HouseFilter.eight, HouseFilter.nine, 
                        HouseFilter.ten, HouseFilter.eleven, HouseFilter.twelve)


        piece_filter = (PieceFilter.one, PieceFilter.two, PieceFilter.three, 
                        PieceFilter.four, PieceFilter.five, PieceFilter.six,
                        PieceFilter.seven, PieceFilter.eight, PieceFilter.nine, 
                        PieceFilter.ten, PieceFilter.eleven, PieceFilter.twelve)



        runner = self.runners_map['low']

        orb_convolutions = [ {idx:runner(orb.format(document=analysis)) }for idx, orb in enumerate(orb_filter)]
        highest_orb_spectrum = list(sorted(orb_convolutions))[:ensemble_size]

        house_convolutions = [ {idx: runner(house.format(document=analysis))} for idx, house in enumerate(house_filter)]
        highest_house_spectrum = list(sorted(house_convolutions))[:ensemble_size]  

        piece_convolutions = [ { piece.__name__: runner(piece.format(document=analysis))} for piece in piece_filter]
        highest_piece_spectrum = list(sorted(piece_convolutions))[:ensemble_size]
        runner = self.runners_map['low']

        orb_convolutions = [ {idx:runner(orb.format(document=analysis)) }for idx, orb in enumerate(orb_filter)]
        highest_orb_spectrum = list(sorted(orb_convolutions))[:ensemble_size]

        basis_collection = []
        position_collections = []
        superposition_collections = []


        fusion = ()
        
        for  element in zip(highest_orb_spectrum, highest_house_spectrum, highest_piece_spectrum):


            if element[0]['dim'] == 2:

                basis_collection.append(
                    fusion(
                        formula=element[0]['formula'] ,
                        acceleration=element[0]['acceleration'],
                        me_1=analysis,
                        me_2=analysis,
                        runners_map=self.runners_map
                    )
                )


                position_collections.append(
                    fusion(
                        formula=element[0]['formula'] ,
                        acceleration=element[0]['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        runners_map=self.runners_map
                    )
                )

                superposition_collections.append(
                    fusion(
                        formula=element[0]['formula'] ,
                        acceleration=element[0]['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        runners_map=self.runners_map
                    )
                )
            
            elif element[0]['dim'] == 3:


                third_mass =  "Original Document:\n" + document + "\nExpert Anlysis:\n" + analysis


                basis_collection.append(
                            fusion(
                                formula=element[0]['formula'] ,
                                acceleration=element[0]['acceleration'],
                                me_1=document,
                                me_2=analysis,
                                me_3 = third_mass,
                                runners_map=self.runners_map
                            )
                        )


                position_collections.append(
                    fusion(
                        formula=element[0]['formula'] ,
                        acceleration=element[0]['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        me_3 = third_mass,
                        runners_map=self.runners_map
                    )
                )

                superposition_collections.append(
                    fusion(
                        formula=element[0]['formula'] ,
                        acceleration=element[0]['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        me_3 = third_mass,
                        runners_map= self.runners_map
                    )
                )


            elif element[0]['dim'] == 4:
                    
                    third_mass = "Original Document:\n" + document + "\nExpert Anlysis:\n" + analysis
                    fourht_mass = document

                    basis_collection.append(
                            fusion(
                                formula=element[1]['formula'] ,
                                acceleration=element[1]['acceleration'],
                                me_1=document,
                                me_2=analysis,
                                me_3 = third_mass,
                                me_4 = fourht_mass,
                                runners_map=self.runners_map
                            )
                        )


                    position_collections.append(
                        fusion(
                            formula=element[1]['formula'] ,
                            acceleration=element[1]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            me_4 = fourht_mass,
                            runners_map=self.runners_map
                        )
                    )

                    superposition_collections.append(
                        fusion(
                            formula=element[1]['formula'] ,
                            acceleration=element[1]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            me_4 = fourht_mass,
                            runners_map= self.runners_map
                        )
                    )


            elif element[1]['dim'] == 2:

                basis_collection.append(
                    fusion(
                        formula=element[1]['formula'] ,
                        acceleration=element[1]['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        runners_map=self.runners_map
                    )
                )


                position_collections.append(
                    fusion(
                        formula=element[1]['formula'] ,
                        acceleration=element[1]['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        runners_map=self.runners_map
                    )
                )

                superposition_collections.append(
                    fusion(
                        formula=element[1]['formula'] ,
                        acceleration=element[1] ['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        runners_map=self.runners_map
                    )
                )
            
            elif element[1]['dim'] == 3:


                third_mass =  "Original Document:\n" + document + "\nExpert Analysis:\n" + analysis


                basis_collection.append(
                            fusion(
                                formula=element[1]['formula'] ,
                                acceleration=element[1]['acceleration'],
                                me_1=document,
                                me_2=analysis,
                                me_3 = third_mass,
                                runners_map=self.runners_map
                            )
                        )


                position_collections.append(
                    fusion(
                        formula=element[1]['formula'] ,
                        acceleration=element[1]['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        me_3 = third_mass,
                        runners_map=self.runners_map
                    )
                )

                superposition_collections.append(
                    fusion(
                        formula=element[1]['formula'] ,
                        acceleration=element[1]['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        me_3 = third_mass,
                        runners_map= self.runners_map
                    )
                )


            elif element[2]['dim'] == 2:
                    
                    third_mass = "Original Document:\n" + document + "\nExpert Analysis:\n" + analysis
                    fourht_mass = document  

                    basis_collection.append(
                            fusion(
                                formula=element[2]['formula'] ,
                                acceleration=element[2]['acceleration'],
                                me_1=document,
                                me_2=analysis,
                                me_3 = third_mass,
                                me_4 = fourht_mass,
                                runners_map=self.runners_map
                            )
                        )


                    position_collections.append(
                        fusion(
                            formula=element[2]['formula'] ,
                            acceleration=element[2]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            me_4 = fourht_mass,
                            runners_map=self.runners_map
                        )
                    )

                    superposition_collections.append(
                        fusion(
                            formula=element[2]['formula'] ,
                            acceleration=element[2]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            me_4 = fourht_mass,
                            runners_map= self.runners_map
                        )
                    )
           


            elif element[2]['dim'] == 3:
                    
                    third_mass = "Original Document:\n" + document + "\nExpert Analysis:\n" + analysis
                    fourht_mass = document  

                    basis_collection.append(
                            fusion(
                                formula=element[2]['formula'] ,
                                acceleration=element[2]['acceleration'],
                                me_1=document,
                                me_2=analysis,
                                me_3 = third_mass,
                                me_4 = fourht_mass,
                                runners_map=self.runners_map
                            )
                        )


                    position_collections.append(
                        fusion(
                            formula=element[2]['formula'] ,
                            acceleration=element[2]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            me_4 = fourht_mass,
                            runners_map=self.runners_map
                        )
                    )

                    superposition_collections.append(
                        fusion(
                            formula=element[2]['formula'] ,
                            acceleration=element[2]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            me_4 = fourht_mass,
                            runners_map= self.runners_map
                        )
                    )
           
            elif element[2]['dim'] == 4:
                    
                    third_mass = "Original Document:\n" + document + "\nExpert Anlysis:\n" + analysis
                    fourht_mass = document  

                    basis_collection.append(
                            fusion(
                                formula=element[2]['formula'] ,
                                acceleration=element[2]['acceleration'],
                                me_1=document,
                                me_2=analysis,
                                me_3 = third_mass,
                                me_4 = fourht_mass,
                                runners_map=self.runners_map
                            )
                        )


                    position_collections.append(
                        fusion(
                            formula=element[2]['formula'] ,
                            acceleration=element[2]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            me_4 = fourht_mass,
                            runners_map=self.runners_map
                        )
                    )

                    superposition_collections.append(
                        fusion(
                            formula=element[2]['formula'] ,
                            acceleration=element[2]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            me_4 = fourht_mass,
                            runners_map= self.runners_map
                        )
                    )
            
                    
        ambiance =  Ensemble(
            basis= basis_collection,
            position = position_collections,
            superposition = superposition_collections
        )


        identity = """

            You are a detective expert in analzying situations and people traits. You describe people perfectly and with great detail.

        """

        prompt = """
            Analyze with great detail the people or character of the following image: what are they wearing? what their face looks like? what impression do they give?. Answer with N/A if the image features no people.
        """ 

        character = runner(identity, prompt, image)

        if len(character) > 50:

            character_filter = (
                CharacterFilter.one, CharacterFilter.two, CharacterFilter.three, CharacterFilter.four,
                CharacterFilter.five, CharacterFilter.six, CharacterFilter.seven, CharacterFilter.eight,
                CharacterFilter.nine, CharacterFilter.ten, CharacterFilter.eleven, CharacterFilter.twelve)

            highest_mbti_character = [ {character.__name__:runner(identity, prompt, image)}for character in character_filter][:1]


            house_filter = (
                HouseFilter.one, HouseFilter.two, HouseFilter.three, HouseFilter.four,
                HouseFilter.five, HouseFilter.six, HouseFilter.seven, HouseFilter.eight,
                HouseFilter.nine, HouseFilter.ten, HouseFilter.eleven, HouseFilter.twelve)
            
            highest_house = [ {house.__name__:runner(identity, prompt, image)}for house in house_filter][:1]


            return ambiance, highest_mbti_character, highest_house 


        else:

            return ambiance

      

    def video_fision(self, video, runners_map, ensemble_size):


        runner = runners_map['video']

        identity = """
            You describe videos.
        """


        prompt = """

            Describe the following video.

        """

        document = runner(identity, prompt, video)
        sys = """

            You are a cinema and media coinosseur with an interest in psychology.
        
        """

        prompt = f"""

            Analyze the following document and provide extensive detailed insight about it juxtaposing it with many references.

                {document} 

        """

        expert = runners_map['high']

        analysis = expert(sys, prompt) 

        orb_filter = (
            OrbFilter.one, OrbFilter.eleven, OrbFilter.twentythree,
            OrbFilter.two, OrbFilter.twelve, OrbFilter.twentyfour,
            OrbFilter.three, OrbFilter.fourteen, OrbFilter.twentyfive,
            OrbFilter.four, OrbFilter.fifteen, OrbFilter.twentysix,
            OrbFilter.five, OrbFilter.sixteen, OrbFilter.twentyseven,
            OrbFilter.six, OrbFilter.seventeen, OrbFilter.twentyeight,
            OrbFilter.seven, OrbFilter.nineteen, OrbFilter.twentynine,
            OrbFilter.eight, OrbFilter.twenty, OrbFilter.thirteen,
            OrbFilter.nine, OrbFilter.twentyone, OrbFilter.thirteenone,
            OrbFilter.tenth, OrbFilter.twentytwo, OrbFilter.thirteentwo,
             OrbFilter.thritythree, OrbFilter.thirtyfour, OrbFilter.thirtyfive,
             OrbFilter.thirtysix
        )


        house_filter = (HouseFilter.one, HouseFilter.two, HouseFilter.three, 
                        HouseFilter.four, HouseFilter.five, HouseFilter.six, 
                        HouseFilter.seven, HouseFilter.eight, HouseFilter.nine, 
                        HouseFilter.ten, HouseFilter.eleven, HouseFilter.twelve)


        piece_filter = (PieceFilter.one, PieceFilter.two, PieceFilter.three, 
                        PieceFilter.four, PieceFilter.five, PieceFilter.six,
                        PieceFilter.seven, PieceFilter.eight, PieceFilter.nine, 
                        PieceFilter.ten, PieceFilter.eleven, PieceFilter.twelve)



        runner = self.runners_map['low']

        orb_convolutions = [ {idx:runner(orb.format(document=analysis)) }for idx, orb in enumerate(orb_filter)]
        highest_orb_spectrum = list(sorted(orb_convolutions))[:ensemble_size]

        house_convolutions = [ {idx: runner(house.format(document=analysis))} for house in enumerate(house_filter)]
        highest_house_spectrum = list(sorted(house_convolutions))[:ensemble_size]  

        piece_convolutions = [ { piece.__name__: runner(piece.format(document=analysis))} for piece in piece_filter]
        highest_piece_spectrum = list(sorted(piece_convolutions))[:ensemble_size]
        fusion = ()
        
        basis_collection = []
        position_collections = []
        superposition_collections = []

        idx = 0

        for  element in zip(highest_orb_spectrum, highest_house_spectrum, highest_piece_spectrum):

            if element[0]['dim'] == 2:

                basis_collection.append(
                    fusion(
                        formula=element[0]['formula'] ,
                        acceleration=element[0]['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        runners_map=self.runners_map
                    )
                )


                position_collections.append(
                    fusion(
                        formula=element[0]['formula'] ,
                        acceleration=element[0]['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        runners_map=self.runners_map
                    )
                )

                superposition_collections.append(
                    fusion(
                        formula=element[0]['formula'] ,
                        acceleration=element[0]['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        runners_map=self.runners_map
                    )
                )
            
            elif element[0]['dim'] == 3:


                third_mass =  "Original Document:\n" + document + "\nExpert Anlysis:\n" + analysis


                basis_collection.append(
                            fusion(
                                formula=element[0]['formula'] ,
                                acceleration=element[0]['acceleration'],
                                me_1=document,
                                me_2=analysis,
                                me_3 = third_mass,
                                runners_map=self.runners_map
                            )
                        )


                position_collections.append(
                    fusion(
                        formula=element[0]['formula'] ,
                        acceleration=element[0]['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        me_3 = third_mass,
                        runners_map=self.runners_map
                    )
                )

                superposition_collections.append(
                    fusion(
                        formula=element[0]['formula'] ,
                        acceleration=element[0]['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        me_3 = third_mass,
                        runners_map= self.runners_map
                    )
                )


            elif element[0]['dim'] == 4:
                    
                    third_mass = "Original Document:\n" + document + "\nExpert Anlysis:\n" + analysis
                    fourht_mass = document

                    basis_collection.append(
                            fusion(
                                formula=element[1]['formula'] ,
                                acceleration=element[1]['acceleration'],
                                me_1=document,
                                me_2=analysis,
                                me_3 = third_mass,
                                me_4 = fourht_mass,
                                runners_map=self.runners_map
                            )
                        )


                    position_collections.append(
                        fusion(
                            formula=element[1]['formula'] ,
                            acceleration=element[1]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            me_4 = fourht_mass,
                            runners_map=self.runners_map
                        )
                    )

                    superposition_collections.append(
                        fusion(
                            formula=element[1]['formula'] ,
                            acceleration=element[1]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            me_4 = fourht_mass,
                            runners_map= self.runners_map
                        )
                    )


            elif element[1]['dim'] == 2:

                basis_collection.append(
                    fusion(
                        formula=element[1]['formula'] ,
                        acceleration=element[1]['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        runners_map=self.runners_map
                    )
                )


                position_collections.append(
                    fusion(
                        formula=element[1]['formula'] ,
                        acceleration=element[1]['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        runners_map=self.runners_map
                    )
                )

                superposition_collections.append(
                    fusion(
                        formula=element[1]['formula'] ,
                        acceleration=element[1] ['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        runners_map=self.runners_map
                    )
                )
            
            elif element[1]['dim'] == 3:


                third_mass =  "Original Document:\n" + document + "\nExpert Analysis:\n" + analysis


                basis_collection.append(
                            fusion(
                                formula=element[1]['formula'] ,
                                acceleration=element[1]['acceleration'],
                                me_1=document,
                                me_2=analysis,
                                me_3 = third_mass,
                                runners_map=self.runners_map
                            )
                        )


                position_collections.append(
                    fusion(
                        formula=element[1]['formula'] ,
                        acceleration=element[1]['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        me_3 = third_mass,
                        runners_map=self.runners_map
                    )
                )

                superposition_collections.append(
                    fusion(
                        formula=element[1]['formula'] ,
                        acceleration=element[1]['acceleration'],
                        me_1=document,
                        me_2=analysis,
                        me_3 = third_mass,
                        runners_map= self.runners_map
                    )
                )


            elif element[2]['dim'] == 2:
                    
                    third_mass = "Original Document:\n" + document + "\nExpert Analysis:\n" + analysis
                    fourht_mass = document  

                    basis_collection.append(
                            fusion(
                                formula=element[2]['formula'] ,
                                acceleration=element[2]['acceleration'],
                                me_1=document,
                                me_2=analysis,
                                me_3 = third_mass,
                                me_4 = fourht_mass,
                                runners_map=self.runners_map
                            )
                        )


                    position_collections.append(
                        fusion(
                            formula=element[2]['formula'] ,
                            acceleration=element[2]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            me_4 = fourht_mass,
                            runners_map=self.runners_map
                        )
                    )

                    superposition_collections.append(
                        fusion(
                            formula=element[2]['formula'] ,
                            acceleration=element[2]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            me_4 = fourht_mass,
                            runners_map= self.runners_map
                        )
                    )
           


            elif element[2]['dim'] == 3:
                    
                    third_mass = "Original Document:\n" + document + "\nExpert Analysis:\n" + analysis
                    fourht_mass = document  

                    basis_collection.append(
                            fusion(
                                formula=element[2]['formula'] ,
                                acceleration=element[2]['acceleration'],
                                me_1=document,
                                me_2=analysis,
                                me_3 = third_mass,
                                me_4 = fourht_mass,
                                runners_map=self.runners_map
                            )
                        )


                    position_collections.append(
                        fusion(
                            formula=element[2]['formula'] ,
                            acceleration=element[2]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            me_4 = fourht_mass,
                            runners_map=self.runners_map
                        )
                    )

                    superposition_collections.append(
                        fusion(
                            formula=element[2]['formula'] ,
                            acceleration=element[2]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            me_4 = fourht_mass,
                            runners_map= self.runners_map
                        )
                    )
           
            elif element[2]['dim'] == 4:
                    
                    third_mass = "Original Document:\n" + document + "\nExpert Anlysis:\n" + analysis
                    fourht_mass = document  

                    basis_collection.append(
                            fusion(
                                formula=element[2]['formula'] ,
                                acceleration=element[2]['acceleration'],
                                me_1=document,
                                me_2=analysis,
                                me_3 = third_mass,
                                me_4 = fourht_mass,
                                runners_map=self.runners_map
                            )
                        )


                    position_collections.append(
                        fusion(
                            formula=element[2]['formula'] ,
                            acceleration=element[2]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            me_4 = fourht_mass,
                            runners_map=self.runners_map
                        )
                    )

                    superposition_collections.append(
                        fusion(
                            formula=element[2]['formula'] ,
                            acceleration=element[2]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            me_4 = fourht_mass,
                            runners_map= self.runners_map
                        )
                    )
            
                    
        ambiance =  Ensemble(
            basis= basis_collection,
            position = position_collections,
            superposition = superposition_collections
        )

        identity = """

            You are a detective expert in analzying situations and people traits. You describe people perfectly and with great detail.

        """

        prompt = """
            Analyze with great detail the people or character of the following video: what are they wearing? what their face looks like? what impression do they give?. Answer with N/A if the image features no people.
        """ 
        runner = self.runners_map['video']
        character = runner(identity, prompt, video)

        if len(character) > 50:

            character_filter = (
                CharacterFilter.one, CharacterFilter.two, CharacterFilter.three, CharacterFilter.four,
                CharacterFilter.five, CharacterFilter.six, CharacterFilter.seven, CharacterFilter.eight,
                CharacterFilter.nine, CharacterFilter.ten, CharacterFilter.eleven, CharacterFilter.twelve)

            highest_mbti_character = [ {character.__name__:runner(identity, prompt, video)}for character in character_filter][:1]


            house_filter = (
                HouseFilter.one, HouseFilter.two, HouseFilter.three, HouseFilter.four,
                HouseFilter.five, HouseFilter.six, HouseFilter.seven, HouseFilter.eight,
                HouseFilter.nine, HouseFilter.ten, HouseFilter.eleven, HouseFilter.twelve)
            
            highest_house = [ {house.__name__:runner(identity, prompt, video)}for house in house_filter][:1]


            return ambiance, highest_mbti_character, highest_house 

        else:


            return ambiance




    def music_fision(self,song , runners_map, ensemble_size, chunk_size):
 

        runner = runners_map['music']

        identity = """
            You describe music snippets.
        """


        prompt = """

            Describe the following music snippet.

        """

        orb_filter = (
            OrbFilter.one, OrbFilter.eleven, OrbFilter.twentythree,
            OrbFilter.two, OrbFilter.twelve, OrbFilter.twentyfour,
            OrbFilter.three, OrbFilter.fourteen, OrbFilter.twentyfive,
            OrbFilter.four, OrbFilter.fifteen, OrbFilter.twentysix,
            OrbFilter.five, OrbFilter.sixteen, OrbFilter.twentyseven,
            OrbFilter.six, OrbFilter.seventeen, OrbFilter.twentyeight,
            OrbFilter.seven, OrbFilter.nineteen, OrbFilter.twentynine,
            OrbFilter.eight, OrbFilter.twenty, OrbFilter.thirteen,
            OrbFilter.nine, OrbFilter.twentyone, OrbFilter.thirteenone,
            OrbFilter.tenth, OrbFilter.twentytwo, OrbFilter.thirteentwo,
            OrbFilter.thritythree, OrbFilter.thirtyfour, OrbFilter.thirtyfive,
            OrbFilter.thirtysix
        )


        house_filter = (HouseFilter.one, HouseFilter.two, HouseFilter.three, 
                        HouseFilter.four, HouseFilter.five, HouseFilter.six, 
                        HouseFilter.seven, HouseFilter.eight, HouseFilter.nine, 
                        HouseFilter.ten, HouseFilter.eleven, HouseFilter.twelve)


        piece_filter = (PieceFilter.one, PieceFilter.two, PieceFilter.three, 
                        PieceFilter.four, PieceFilter.five, PieceFilter.six,
                        PieceFilter.seven, PieceFilter.eight, PieceFilter.nine, 
                        PieceFilter.ten, PieceFilter.eleven, PieceFilter.twelve)





        snippets = self._fragment(song, chunk_size)

        for snippet in snippets:

            document = runner(identity, prompt, snippet)

            sys = """

                You are a music coinosseur with an interest in psychology.
            
            """

            prompt = f"""

                Analyze the following document and provide extensive detailed insight about it juxtaposing it with many references.

                    {document} 

            """

            expert = runners_map['high']

            analysis = expert(sys, prompt) 
            runner = self.runners_map['low']

            orb_convolutions = [ {idx:runner(orb.format(document=analysis)) }for idx, orb in enumerate(orb_filter)]
            highest_orb_spectrum = list(sorted(orb_convolutions))[:ensemble_size]

            house_convolutions = [ {idx: runner(house.format(document=analysis))} for house in enumerate(house_filter)]
            highest_house_spectrum = list(sorted(house_convolutions))[:ensemble_size]  

            piece_convolutions = [ { piece.__name__: runner(piece.format(document=analysis))} for piece in piece_filter]
            highest_piece_spectrum = list(sorted(piece_convolutions))[:ensemble_size]
            fusion = Reduce().fusion
            
            basis_collection = []
            position_collections = []
            superposition_collections = []

            idx = 0

            for  element in zip(highest_orb_spectrum, highest_house_spectrum, highest_piece_spectrum):

                if element[0]['dim'] == 2:

                    basis_collection.append(
                        fusion(
                            formula=element[0]['formula'] ,
                            acceleration=element[0]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            runners_map=self.runners_map
                        )
                    )


                    position_collections.append(
                        fusion(
                            formula=element[0]['formula'] ,
                            acceleration=element[0]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            runners_map=self.runners_map
                        )
                    )

                    superposition_collections.append(
                        fusion(
                            formula=element[0]['formula'] ,
                            acceleration=element[0]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            runners_map=self.runners_map
                        )
                    )
                
                elif element[0]['dim'] == 3:


                    third_mass =  "Original Document:\n" + document + "\nExpert Anlysis:\n" + analysis


                    basis_collection.append(
                                fusion(
                                    formula=element[0]['formula'] ,
                                    acceleration=element[0]['acceleration'],
                                    me_1=document,
                                    me_2=analysis,
                                    me_3 = third_mass,
                                    runners_map=self.runners_map
                                )
                            )


                    position_collections.append(
                        fusion(
                            formula=element[0]['formula'] ,
                            acceleration=element[0]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            runners_map=self.runners_map
                        )
                    )

                    superposition_collections.append(
                        fusion(
                            formula=element[0]['formula'] ,
                            acceleration=element[0]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            runners_map= self.runners_map
                        )
                    )


                elif element[0]['dim'] == 4:
                        
                        third_mass = "Original Document:\n" + document + "\nExpert Anlysis:\n" + analysis
                        fourht_mass = document

                        basis_collection.append(
                                fusion(
                                    formula=element[1]['formula'] ,
                                    acceleration=element[1]['acceleration'],
                                    me_1=document,
                                    me_2=analysis,
                                    me_3 = third_mass,
                                    me_4 = fourht_mass,
                                    runners_map=self.runners_map
                                )
                            )


                        position_collections.append(
                            fusion(
                                formula=element[1]['formula'] ,
                                acceleration=element[1]['acceleration'],
                                me_1=document,
                                me_2=analysis,
                                me_3 = third_mass,
                                me_4 = fourht_mass,
                                runners_map=self.runners_map
                            )
                        )

                        superposition_collections.append(
                            fusion(
                                formula=element[1]['formula'] ,
                                acceleration=element[1]['acceleration'],
                                me_1=document,
                                me_2=analysis,
                                me_3 = third_mass,
                                me_4 = fourht_mass,
                                runners_map= self.runners_map
                            )
                        )


                elif element[1]['dim'] == 2:

                    basis_collection.append(
                        fusion(
                            formula=element[1]['formula'] ,
                            acceleration=element[1]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            runners_map=self.runners_map
                        )
                    )


                    position_collections.append(
                        fusion(
                            formula=element[1]['formula'] ,
                            acceleration=element[1]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            runners_map=self.runners_map
                        )
                    )

                    superposition_collections.append(
                        fusion(
                            formula=element[1]['formula'] ,
                            acceleration=element[1] ['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            runners_map=self.runners_map
                        )
                    )
                
                elif element[1]['dim'] == 3:


                    third_mass =  "Original Document:\n" + document + "\nExpert Analysis:\n" + analysis


                    basis_collection.append(
                                fusion(
                                    formula=element[1]['formula'] ,
                                    acceleration=element[1]['acceleration'],
                                    me_1=document,
                                    me_2=analysis,
                                    me_3 = third_mass,
                                    runners_map=self.runners_map
                                )
                            )


                    position_collections.append(
                        fusion(
                            formula=element[1]['formula'] ,
                            acceleration=element[1]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            runners_map=self.runners_map
                        )
                    )

                    superposition_collections.append(
                        fusion(
                            formula=element[1]['formula'] ,
                            acceleration=element[1]['acceleration'],
                            me_1=document,
                            me_2=analysis,
                            me_3 = third_mass,
                            runners_map= self.runners_map
                        )
                    )


                elif element[2]['dim'] == 2:
                        
                        third_mass = "Original Document:\n" + document + "\nExpert Analysis:\n" + analysis
                        fourht_mass = document  

                        basis_collection.append(
                                fusion(
                                    formula=element[2]['formula'] ,
                                    acceleration=element[2]['acceleration'],
                                    me_1=document,
                                    me_2=analysis,
                                    me_3 = third_mass,
                                    me_4 = fourht_mass,
                                    runners_map=self.runners_map
                                )
                            )


                        position_collections.append(
                            fusion(
                                formula=element[2]['formula'] ,
                                acceleration=element[2]['acceleration'],
                                me_1=document,
                                me_2=analysis,
                                me_3 = third_mass,
                                me_4 = fourht_mass,
                                runners_map=self.runners_map
                            )
                        )

                        superposition_collections.append(
                            fusion(
                                formula=element[2]['formula'] ,
                                acceleration=element[2]['acceleration'],
                                me_1=document,
                                me_2=analysis,
                                me_3 = third_mass,
                                me_4 = fourht_mass,
                                runners_map= self.runners_map
                            )
                        )
            


                elif element[2]['dim'] == 3:
                        
                        third_mass = "Original Document:\n" + document + "\nExpert Analysis:\n" + analysis
                        fourht_mass = document  

                        basis_collection.append(
                                fusion(
                                    formula=element[2]['formula'] ,
                                    acceleration=element[2]['acceleration'],
                                    me_1=document,
                                    me_2=analysis,
                                    me_3 = third_mass,
                                    me_4 = fourht_mass,
                                    runners_map=self.runners_map
                                )
                            )


                        position_collections.append(
                            fusion(
                                formula=element[2]['formula'] ,
                                acceleration=element[2]['acceleration'],
                                me_1=document,
                                me_2=analysis,
                                me_3 = third_mass,
                                me_4 = fourht_mass,
                                runners_map=self.runners_map
                            )
                        )

                        superposition_collections.append(
                            fusion(
                                formula=element[2]['formula'] ,
                                acceleration=element[2]['acceleration'],
                                me_1=document,
                                me_2=analysis,
                                me_3 = third_mass,
                                me_4 = fourht_mass,
                                runners_map= self.runners_map
                            )
                        )
            
                elif element[2]['dim'] == 4:
                        
                        third_mass = "Original Document:\n" + document + "\nExpert Anlysis:\n" + analysis
                        fourht_mass = document  

                        basis_collection.append(
                                fusion(
                                    formula=element[2]['formula'] ,
                                    acceleration=element[2]['acceleration'],
                                    me_1=document,
                                    me_2=analysis,
                                    me_3 = third_mass,
                                    me_4 = fourht_mass,
                                    runners_map=self.runners_map
                                )
                            )


                        position_collections.append(
                            fusion(
                                formula=element[2]['formula'] ,
                                acceleration=element[2]['acceleration'],
                                me_1=document,
                                me_2=analysis,
                                me_3 = third_mass,
                                me_4 = fourht_mass,
                                runners_map=self.runners_map
                            )
                        )

                        superposition_collections.append(
                            fusion(
                                formula=element[2]['formula'] ,
                                acceleration=element[2]['acceleration'],
                                me_1=document,
                                me_2=analysis,
                                me_3 = third_mass,
                                me_4 = fourht_mass,
                                runners_map= self.runners_map
                            )
                        )
                
                        
            ambiance =  Ensemble(
                basis= basis_collection,
                position = position_collections,
                superposition = superposition_collections
            )

       

        return ambiance





