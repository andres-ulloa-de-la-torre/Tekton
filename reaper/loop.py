from map import FunctionMapper
from token_count import TokenCount
from containers import Ensemble
from parsers import parse_formulae, divide_formulae
from util.identifiers import Elements, Modalities, Signs
from util.context_mapppers import map_coefficient_to_ctx_size, map_coefficient_to_rag_k, map_document_size_to_n_summary_paragraphs 
from util.runners import RAG, TextRunner, SDXLRunner, SDXLTurboRunner, FluxRunner, LlavaRunner
from filter import PieceFilter, OrbFilter, HouseFilter, CharacterFilter
from reduce import Reduce, JungianActivationFunctions, JungianObjectReducer
import matplotlib.image as mpimg
from PIL import Image



db = FunctionMapper()

SPEED_OF_SE = 512


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

