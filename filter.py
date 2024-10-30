

class Rerankers:


     @classmethod
     def rerank(specification, behavior):


        identity = """
            You are an expert psychologyst working on a development project with comoputer assisted psychology and you assess how much a behavioral specification matches the displayed behavior by the computational agent.


            Score from 1 to 100 how much a behavioral specification matches the behavior by the computational agent.

            Score from i to 100 how much is the agent hallucinating.

            Answer with only a json document with keys 'hallucination' and 'relevance'.
                    
        """

        prompt = f"""

            Behavior specification:

                {specification}


            Performed behavior:

                {behavior} 

        """


        return identity, prompt




class HouseFilter:



    @classmethod
    def one(document):

        identity = """
            You are an expert astrologer and tarot reader. You rank from 1 to 100 how well the following document describes scenarios of house one. 

            Answer with only the score.
        """

        prompt = f"""

            {document} 

        """


        return identity, prompt, "ONE"


    @classmethod
    def two(document):

        identity = """
            You are an expert astrologer and tarot reader. You rank from 1 to 100 how well the following document describes scenarios of house two. 

            Answer with only the score.
        """

        prompt = f"""

            {document}

        """


        return identity , prompt, "TWO"
    


    @classmethod
    def three(document):

        identity = """
            You are an expert astrologer and tarot reader. You rank from 1 to 100 how well the following document describes scenarios of house three.   

            Answer with only the score.
        """

        prompt = f"""

            {document}

        """


        return identity, prompt, "THREE"
    

    @classmethod
    def four(document):

        identity = """
            You are an expert astrologer and tarot reader. You rank from 1 to 100 how well the following document describes scenarios of house four.

            Answer with only the score.
        """

        prompt = f"""

            {document}

        """


        return identity, prompt, "FOUR"
    

    @classmethod
    def five(document):

        identity = """
            You are an expert astrologer and tarot reader. You rank from 1 to 100 how well the following document describes scenarios of house five.

            Answer with only the score.
        """

        prompt = f"""

            {document}

        """

        return identity,  prompt, "FIVE"
    
    @classmethod
    def six(document):

        identity = """
            You are an expert astrologer and tarot reader. You rank from 1 to 100 how well the following document describes scenarios of house six.

            Answer with only the score.
        """

        prompt = f"""

            {document}

        """

        return identity,  prompt, "SIX" 
    

    @classmethod
    def seven(document):

        identity = """
            You are an expert astrologer and tarot reader. You rank from 1 to 100 how well the following document describes scenarios of house seven.

            Answer with only the score.
        """

        prompt = f"""

            {document}

        """

        return identity,  prompt, "SEVEN"
    

    @classmethod
    def eight(document):

        identity = """
            You are an expert astrologer and tarot reader. You rank from 1 to 100 how well the following document describes scenarios of house eight.

            Answer with only the score.
        """

        prompt = f"""

            {document}

        """

        return identity,  prompt, "EIGHT"
    

    @classmethod
    def nine(document):

        identity = """
            You are an expert astrologer and tarot reader. You rank from 1 to 100 how well the following document describes scenarios of house nine.

            Answer with only the score.
        """

        prompt = f"""

            {document}

        """

        return identity,  prompt, "NINE"
    

    @classmethod
    def ten(document):

        identity = """
            You are an expert astrologer and tarot reader. You rank from 1 to 100 how well the following document describes scenarios of house ten.

            Answer with only the score.
        """

        prompt = f"""

            {document}

        """

        return identity,  prompt, "TEN"
    



    @classmethod
    def eleven(document):

        identity = """
            You are an expert astrologer and tarot reader. You rank from 1 to 100 how well the following document describes scenarios of house eleven.

            Answer with only the score.
        """

        prompt = f"""

            {document}

        """

        return identity,  prompt, "ELEVEN"




    @classmethod
    def twelve(document):

        identity = """
            You are an expert astrologer and tarot reader. You rank from 1 to 100 how well the following document describes scenarios of house twelve.

            Answer with only the score.
        """

        prompt = f"""

            {document}

        """

        return identity,  prompt, "TWELVE"






class AxesFilter:


    @classmethod
    def ego(document):

        identity = """

            You are a analytical psychologist.

        """

        prompt = """

            Score from 0 to 100 how high the subject performing in the following scenario is refering and establishing the boundaries of his own identity aswell as being creative.

            Answer only with the score.

            Document:

            {document}

        """

        return identity,  prompt, "EGO"


    @classmethod
    def superego(document):

        identity = """

            You are a analytical psychologist.

        """

        prompt = """

            Score from 0 to 100 how high the subject performing in the following scenario is being productive yet destructive and defensive towards others peoples intentions.

            Answer only with the score.

            Document:

            {document}

        """

        return identity,  prompt, "SUPEREGO"


    @classmethod
    def shadow(document):

        identity = """

            You are a analytical psychologist.

        """

        prompt = """

            Score from 0 to 100 how high the subject performing in the following scenario is behaving without comprehension creating problems instead of solving them.

            Answer only with the score.

            Document:

            {document}

        """

        return identity,  prompt, "SHADOW"


    @classmethod
    def spirit(document):

        identity = """

            You are a analytical psychologist.

        """

        prompt = """

            Score from 0 to 100 how high the subject performing in the following scenario is behaving with regards to goal, inspiration and means to transform into something greater. 

            Answer only with the score.

            Document:

            {document}

        """

        return identity,  prompt, "SHADOW"





class PieceFilter:


    @classmethod
    def one(document):

        identity = """
            You are a metaphysics philospher seeking to relate situations and people to a higher utilitarian conception which makes them tools.
        """

        prompt = """

            Score from 0 to 100 how high the following document relates the subject or subjects to a sword or a helmet.

            Answer only with the score.

            Document:

            {document}


        """

        return identity,  prompt, "SWORD/HELMET"

    @classmethod
    def two(document):
        
        identity = """
            You are a metaphysics philospher seeking to relate situations and people to a higher utilitarian conception which makes them tools.
        """

        prompt = """

            Score from 0 to 100 how high the following document relates the subject or subjects to a shield.

            Answer only with the score.

            Document:

            {document}


        """

        return identity,  prompt, "SHIELD"



    @classmethod
    def three(document):
        identity = """
            You are a metaphysics philospher seeking to relate situations and people to a higher utilitarian conception which makes them tools.
        """

        prompt = """

            Score from 0 to 100 how high the following document relates the subject or subjects to horn.

            Answer only with the score.

            Document:

            {document}


        """

        return identity,  prompt, "HORN"



    @classmethod
    def four(document):
        
        identity = """
            You are a metaphysics philospher seeking to relate situations and people to a higher utilitarian conception which makes them tools.
        """

        prompt = """

            Score from 0 to 100 how high the following document relates the subject or subjects to an amulet.

            Answer only with the score.

            Document:

            {document}


        """

        return identity,  prompt, "AMULET"




    @classmethod
    def five():
        identity = """
            You are a metaphysics philospher seeking to relate situations and people to a higher utilitarian conception which makes them tools.
        """

        prompt = """

            Score from 0 to 100 how high the following document relates the subject or subjects to 'eyes' or 'torch'.

            Answer only with the score.

            Document:

            {document}


        """

        return identity,  prompt, "TORCH/EYES"




    @classmethod
    def six():
        
        identity = """
            You are a metaphysics philospher seeking to relate situations and people to a higher utilitarian conception which makes them tools.
        """

        prompt = """

            Score from 0 to 100 how high the following document relates the subject or subjects to 'ring' or 'perfection'.

            Answer only with the score.

            Document:

            {document}


        """

        return identity,  prompt, "PERFECTION/RING"






    @classmethod
    def seven():
        identity = """
            You are a metaphysics philospher seeking to relate situations and people to a higher utilitarian conception which makes them tools.
        """

        prompt = """

            Score from 0 to 100 how high the following document relates the subject or subjects to 'diadem' or 'musical instrument'.

            Answer only with the score.

            Document:

            {document}


        """

        return identity,  prompt, "DIAMOND/HARP"






    @classmethod
    def eight():
        identity = """
            You are a metaphysics philospher seeking to relate situations and people to a higher utilitarian conception which makes them tools.
        """

        prompt = """

            Score from 0 to 100 how high the following document relates the subject or subjects to 'spear' or 'dagger'.

            Answer only with the score.

            Document:

            {document}


        """

        return identity,  prompt , "SPEAR/DAGGER"



    @classmethod
    def nine():
        identity = """
            You are a metaphysics philospher seeking to relate situations and people to a higher utilitarian conception which makes them tools.
        """

        prompt = """

            Score from 0 to 100 how high the following document relates the subject or subjects to 'thig guards'.

            Answer only with the score.

            Document:

            {document}


        """

        return identity,  prompt, "THIGH GUARDS"


    @classmethod
    def ten():
        
        identity = """
            You are a metaphysics philospher seeking to relate situations and people to a higher utilitarian conception which makes them tools.
        """

        prompt = """

            Score from 0 to 100 how high the following document relates the subject or subjects to 'clock' or 'boots'.

            Answer only with the score.

            Document:

            {document}


        """

        return identity,  prompt, "CLOCK/BOOTS"



    @classmethod
    def eleven():
        identity = """
            You are a metaphysics philospher seeking to relate situations and people to a higher utilitarian conception which makes them tools.
        """

        prompt = """

            Score from 0 to 100 how high the following document relates the subject or subjects to 'breastplate'

            Answer only with the score.

            Document:

            {document}


        """

        return identity,  prompt, "BREASTPLATE"




    @classmethod
    def twelve():
        
        identity = """
            You are a metaphysics philospher seeking to relate situations and people to a higher utilitarian conception which makes them tools.
        """

        prompt = """

            Score from 0 to 100 how high the following document relates the subject or subjects to 'mask'

            Answer only with the score.

            Document:

            {document}


        """

        return identity,  prompt, "MASK"




      


class HouseFilter:

    pass
    
 


class OrbFilter:
    
    @classmethod
    def one(self, document):  

        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""

            Score from 1 to 100 how 'lascerating' the following document is to the reader and subjects involved. Answer with only the score.

                {document}

        """


        return identity,  prompt

    @classmethod
    def two(self, document):
        
        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""

            Score from 1 to 100 how 'lascerating' the following document is to the reader and subjects involved. Answer with only the score.

                {document}

        """


        return identity,  prompt


    @classmethod
    def three(self, document):
        
        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""

            Score from 1 to 100 how 'bludgeoning' the following document is to the reader and subjects involved. Answer with only the score.

                {document}

        """


        return identity,  prompt


    @classmethod
    def four(self, document):
        
        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""

            Score from 1 to 100 how 'absorbing' the following document is to the reader in a sense of protecting and shileding, and the subjects involved. Answer with only the score.

                {document}

        """


        return identity,  prompt


    @classmethod
    def five(self, document):
        
        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""

            Score from 1 to 100 how 'immobile' is the following document  to the reader in a sense of stating immobility towards the subjects intention. Answer with only the score.

                {document}

        """


        return identity,  prompt



    @classmethod
    def six(self, document):
        
        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""

            Score from 1 to 100 how the following document evokes 'dust' to the reader in a sense of stating muliplicity and pulverization of unity into multiplicity. Answer with only the score.

                {document}

        """


        return identity,  prompt


    @classmethod
    def seven(self, document):
        
        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""

            Score from 1 to 100 how the following document evokes 'resonance' to the reader in a sense of making the subjects and reader resonate and communicate with each other. Answer with only the score.

                {document}

        """


        return identity,  prompt



    @classmethod
    def eight(self, document):
        
        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""

            Score from 1 to 100 how the following document evokes 'echoes' to the reader in a sense of making the subjects and reader  repeat each other while dampening and dilluting the original message. Answer with only the score.

                {document}

        """


        return identity,  prompt



    @classmethod
    def nine(self, document):
        
        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""

            Score from 1 to 100 how the following document evokes 'whispering' to the reader in a sense of making the subjects and reader to communicate a hidden message. Answer with only the score.

                {document}

        """


        return identity,  prompt




    @classmethod
    def ten(self, document):

        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""
            
            Score from 1 to 100 how the following document evokes 'rain' to the reader in a sense of making the subjects and reader being granted elasticity and togetherness from a factor above. Answer with only the score.

                {document}

        """

  
    @classmethod
    def eleven(self, document):

        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""
            
            Score from 1 to 100 how the following document evokes 'river' to the reader in a sense of making the subjects and reader being granted granted a strong and flowing sense of emotion. Answer with only the score.

                {document}

        """

        return identity,  prompt

  
    @classmethod
    def twelve(self, document):

        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""
            
            Score from 1 to 100 how the following document evokes 'roots' to the reader in a sense of making the subjects and reader being nurtured from a humbling or humble factor below. 
            
            Answer with only the score.

                {document}

        """

        return identity,  prompt

  
    @classmethod
    def thirtheen(self, document):

        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""
            
            Score from 1 to 100 how the following document evokes 'trunk' or 'wand' to the reader in a sense of making the subjects and reader feel sovereign within their own means and supported by their own strenght. 
            
            Answer with only the score.

                {document}

        """

        return identity,  prompt


    @classmethod
    def fourteen(self, document):
        
        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""
            
            Score from 1 to 100 how the following document evokes 'light' to the reader in a sense of making the subjects and reader experience with <<clarity>> the qualities or glory of something. 
            
            Answer with only the score.

                {document}

        """

        return identity,  prompt


    @classmethod
    def fifteen(self, document):
        
        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""
            
            Score from 1 to 100 how the following document evokes 'thunder' to the reader in a sense of making the subjects and reader experience the overwhelming and excessive nature of a realization about a specific individual. 
            
            Answer with only the score.

                {document}

        """

        return identity,  prompt



    @classmethod
    def sixteen(self, document):

        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """
        prompt = f"""
            
            Score from 1 to 100 how the following document evokes 'charring' to the reader in a sense of making the subjects and reader experience the details of what they have done wrong. 
            
            Answer with only the score.

                {document}

        """

        return identity,  prompt

    @classmethod
    def seventeen(self, document):

        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """
        prompt = f"""
            
            Score from 1 to 100 how the following document evokes 'filtering' to the reader in a sense of making the subjects and reader experience the details by which they can get rid of the negative consequences of their actions. 
            
            Answer with only the score.

                {document}

        """

        return identity,  prompt

    @classmethod
    def eighteen(self, document):

        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """
        prompt = f"""
            
            Score from 1 to 100 how the following document evokes 'crystallization' to the reader in a sense of making the subjects and reader experience the results of detailed oriented restoration towards themselves and other people. 
            
            Answer with only the score.

                {document}

        """

        return identity,  prompt

    @classmethod
    def nineteen(self, document):

        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """
        prompt = f"""
            
            Score from 1 to 100 how the following document evokes 'rythm' to the reader in a sense of making the subjects and reader be synchronized with each other in a manner thats fair and symnetrical. 
            
            Answer with only the score.

                {document}

        """

        return identity,  prompt



    @classmethod
    def twenty(self, document):

        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """
        prompt = f"""
            
            Score from 1 to 100 how the following document evokes 'wind' to the reader in a sense of making the subjects and reader experience a release of an unfair burden. 
            
            Answer with only the score.

                {document}

        """

        return identity,  prompt

    @classmethod
    def twentyone(self, document):

        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """
        prompt = f"""
            
            Score from 1 to 100 how the following document evokes 'hailstorm' to the reader in a sense of making the subjects and reader experience deep emotional turmoil.
            
            Answer with only the score.

                {document}

        """

        return identity,  prompt


    @classmethod
    def twentytwo(self, document):

        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """
        prompt = f"""
            
            Score from 1 to 100 how the following document evokes 'ice' to the reader in a sense of making the subjects and reader experience coldness, distance and 
            
            Answer with only the score.

                {document}

        """

        return identity,  prompt


    @classmethod
    def twentythree(self, document):

        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""


            Score from 1 to 100 how the following document evokes 'phoenix' to the reader in a sense of making the subjects and reader experience glorification at the expense of the destruction of something.

            Answer with only the score.

                {document}      


        """

        return identity,  prompt

    @classmethod
    def twentyfour(self, document):

        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""


            Score from 1 to 100 how the following document evokes 'poison' to the reader in a sense of making the subjects and reader experience the slow corruption of something changing its state through death into a new one. 

            Answer with only the score.

                {document}      


        """

        return identity,  prompt



    @classmethod
    def twentyfive(self, document):

        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""


            Score from 1 to 100 how the following document evokes 'piercing' to the reader in a sense of making the subjects and reader experience the aggresive penetration of a belief so its challenged into a new one. 

            Answer with only the score.

                {document}      


        """

        return identity,  prompt

    @classmethod
    def twentysix(self, document):

        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""

            Score from 1 to 100 how the following document evokes 'firestorm' to the reader in a sense of making the subjects and reader experience an expansive belief that devours and takes over all the subjects.

            Answer with only the score.

                {document}      


        """

        return identity,  prompt

    @classmethod
    def twentyseven(self, document):

        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""

            Score from 1 to 100 how the following document evokes 'meteor' to the reader in a sense of making the subjects and reader experience the sense that a message of belief is descending upon themselves from a higher perspective.

            Answer with only the score.

                {document}      


        """

        return identity,  prompt

    @classmethod
    def twentyeight(self, document):

        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""

            Score from 1 to 100 how the following document evokes 'earthquake'  to the reader in a sense of making the subjects and reader experience the sense that the subjects and reader are shaken  in all their  foundational beliefs.

            Answer with only the score.

                {document}      


        """

        return identity,  prompt



    @classmethod
    def twentynine(self, document):

        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""

            Score from 1 to 100 how the following document evokes 'fall' ir 'gravity' to the reader in a sense of making the subjects and reader experience the sense that their actions all submit to unevitable consequences.

            Answer with only the score.

                {document}      


        """

        return identity,  prompt


    @classmethod
    def thirty(self, document):

        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""

            Score from 1 to 100 how the following document evokes 'time' to the reader in a sense of making the subjects and reader experience the sense that time is passing and consequences are collectively getting worse.

            Answer with only the score.

                {document}      


        """

        return identity,  prompt

    @classmethod
    def thirtyone(self, document):

        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""

            Score from 1 to 100 how the following document evokes 'static' to the reader in a sense of making the subjects and reader experience the buildup of some important event about to happen.

            Answer with only the score.

                {document}      


        """

        return identity,  prompt


    @classmethod
    def thirtytwo(self, document):

        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""

            Score from 1 to 100 how the following document evokes 'greatsword' to the reader in a sense of making the subjects and reader experience a sense of empowering equality, symmetry and logical precision.

            Answer with only the score.

                {document}      


        """

        return identity,  prompt

    @classmethod
    def thirtythree(self, document):

        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""

            Score from 1 to 100 how the following document evokes 'shadows' to the reader in a sense of making the subjects and reader experience a sense of fear and uncertainty of what their identity is with regards to their past actions.

            Answer with only the score.

                {document}      


        """

        return identity,  prompt

    @classmethod
    def thirtyfour(self, document):

        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""

            Score from 1 to 100 how the following document evokes 'ghost' to the reader in a sense of making the subjects and reader experience a 

            Answer with only the score.

                {document}      


        """

        return identity,  prompt

    @classmethod
    def thirtyfive(self, document):

        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""

            Score from 1 to 100 how the following document evokes 'vacuum' to the reader in a sense of making the subjects and reader experience internal emptyness.

            Answer with only the score.

                {document}      


        """

        return identity,  prompt

    @classmethod
    def thirtysix(self, document):

        identity = """

            You are a philosopher seeking to score how closely human situations match meta-physical phenomena.

        """

        prompt = f"""

            Score from 1 to 100 how the following document evokes 'lighting' to the reader in a sense of making the subjects and reader experience a flash of togetherness pulling two aspects, worlds or a pattern together in glory and opportuniyy.

            Answer with only the score.

                {document}      


        """

        return identity,  prompt








class CharacterFiler:



    @classmethod
    def estp( character):
        
        identity = """
            You are a jungian psychoanalyst.

        """
        prompt = f"""
            
            Score from 1 to 100 how the following characterd resembles a gladiator. An ESTP.

            Answer with only the score.

                {character}      

        """

        return identity,  prompt


    @classmethod
    def esfp( character):
         
        identity = """
            You are a jungian psychoanalyst.

        """
        prompt = f"""
            
            Score from 1 to 100 how the following characterd resembles an actor and entertainer. An ESFP.

            Answer with only the score.

                {character}      

        """

        return identity,  prompt

       

    @classmethod
    def istp( character):
        identity = """
            You are a jungian psychoanalyst.

        """
        prompt = f"""
            
            Score from 1 to 100 how the following characterd resembles an artificer. An ISTP.

            Answer with only the score.

                {character}      

        """

        return identity,  prompt

 


    @classmethod
    def isfp( character):
        identity = """
            You are a jungian psychoanalyst.

        """
        prompt = f"""
            
            Score from 1 to 100 how the following characterd resembles an artist. An ISFP.
            Answer with only the score.

                {character}      

        """

        return identity,  prompt




    @classmethod
    def infp( character):
        identity = """
            You are a jungian psychoanalyst.

        """
        prompt = f"""
            
            Score from 1 to 100 how the following characterd resembles a healer. An INFP.

            Answer with only the score.

                {character}      

        """

        return identity,  prompt





    @classmethod
    def enfp( character):
        identity = """
            You are a jungian psychoanalyst.

        """
        prompt = f"""
            
            Score from 1 to 100 how the following characterd resembles an idealistic activist. An ENFP.

            Answer with only the score.

                {character}      

        """

        return identity,  prompt

    

    @classmethod
    def entp( character):
        identity = """
            You are a jungian psychoanalyst.

        """
        prompt = f"""
            
            Score from 1 to 100 how the following characterd resembles a devil advocate. An ENTP. 

            Answer with only the score.

                {character}      

        """

        return identity,  prompt

    

    

    @classmethod
    def intp( character):
        
        identity = """
            You are a jungian psychoanalyst.

        """
        prompt = f"""
            
            Score from 1 to 100 how the following characterd resembles a curious but awkward scientist. An INTP.

            Answer with only the score.

                {character}      

        """

        return identity,  prompt

    




    @classmethod
    def infj( character):
        identity = """
            You are a jungian psychoanalyst.

        """
        prompt = f"""
            
            Score from 1 to 100 how the following characterd resembles an humanitarian yet lonely advocate. An INFJ. 

            Answer with only the score.

                {character}      

        """

        return identity,  prompt



    @classmethod
    def enfj( character):
        identity = """
            You are a jungian psychoanalyst.

        """
        prompt = f"""
            
            Score from 1 to 100 how the following characterd resembles an inspiring yet talkative leader. An ENFJ. 

            Answer with only the score.

                {character}      

        """

        return identity,  prompt


    @classmethod
    def entj( character):

        identity = """
            You are a jungian psychoanalyst.

        """
        prompt = f"""
            
            Score from 1 to 100 how the following characterd resembles a commander. An ENTJ. 

            Answer with only the score.

                {character}      

        """

        return identity,  prompt


       
    @classmethod
    def intj( character):
        identity = """
            You are a jungian psychoanalyst.

        """
        prompt = f"""
            
            Score from 1 to 100 how the following characterd resembles an architect. An INTJ. 

            Answer with only the score.

                {character}      

        """

        return identity,  prompt



    @classmethod
    def esfj( character):
        identity = """
            You are a jungian psychoanalyst.

        """
        prompt = f"""
            
            Score from 1 to 100 how the following characterd resembles a cavalier and consul. An ESFJ.

            Answer with only the score.

                {character}      

        """

        return identity,  prompt


    @classmethod
    def istj( character):
        
        identity = """
            You are a jungian psychoanalyst.

        """
        prompt = f"""
            
            Score from 1 to 100 how the following characterd resembles a logician. An ISTJ.

            Answer with only the score.

                {character}      

        """

        return identity,  prompt



    @classmethod
    def isfj( character):
        identity = """
            You are a jungian psychoanalyst.

        """
        prompt = f"""
            
            Score from 1 to 100 how the following characterd resembles a defender. An ISFJ.

            Answer with only the score.

                {character}      

        """

        return identity,  prompt

       


    @classmethod
    def estj( character):

        identity = """
            You are a jungian psychoanalyst.

        """
        prompt = f"""
            
            Score from 1 to 100 how the following characterd resembles a strict manager. An ESTJ.

            Answer with only the score.

                {character}      

        """

        return identity,  prompt

       
