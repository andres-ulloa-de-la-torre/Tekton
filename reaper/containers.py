

from dotenv import load_dotenv
import os 
import praw
import datetime
from map import Integrator, Proportional, Derivator, BiphasicOscillator, TriphasicOscillator, QuadriphasicOscillator, Map
from filter import AxisFilter
from util import types, Signs, Element, Modality
from random import randint
from random import random

load_dotenv()


SPEED_OF_SE = 512

class Events:

    def __init__(self) -> None:

        """
        Initializes an instance of the class with the given parameters.

        The instance is initialized with the Reddit API credentials from the environment variables.

        The Reddit API credentials are obtained from the environment variables.

        Parameters:
            None

        Returns:
            None
        """

        self.reddit =  praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT"),
        )


    def get_events(self, n_events):

        """
        Retrieves the top n_events hot posts from the worldnews subreddit and adds the top 3 comments from each post to a document.
        The document structure is as follows:
        Post title
        Top level comment 1
        Top level comment 2
        Top level comment 3

        Args:
            n_events (int): The number of events to retrieve.

        Returns:
            list: A list of the retrieved documents.
        """
        events = []

        for submission in self.reddit.subreddit("worldnews").hot(limit=n_events):

           top_level_comments = list(submission.comments) 
           document = submission.title + "\n" + top_level_comments[0].body + "\n" + top_level_comments[1].body + "\n" + top_level_comments[2].body
           events.append(document)


        return events




def _map_to_position(house):

    if house == 1:

        return 'Aries'

    elif house == 2:

        return 'Taurus'
    

    elif house == 3:

        return 'Gemini'
    

    elif house == 4:

        return 'Cancer'
    

    elif house == 5:

        return 'Leo'
    

    elif house == 6:

        return 'Virgo'
    

    elif house == 7:

        return 'Libra'
    

    elif house == 8:

        return 'Scorpio'
    

    elif house == 9:

        return 'Sagittarius'
    

    elif house == 10:

        return 'Capricorn'
    

    elif house == 11:

        return 'Aquarius'
    

    elif house == 12:

        return 'Pisces'






class Envelope:


    def __init__(self, basis, position , superposition) -> None:
        """
        Initializes a new instance of the Envelope class.

        Args:
            basis (BiphasicOscillator | TriphasicOscillator | QuadriphasicOscillator): The basis of the envelope.
            position (BiphasicOscillator | TriphasicOscillator | QuadriphasicOscillator): The position of the envelope.
            superposition (BiphasicOscillator | TriphasicOscillator | QuadriphasicOscillator): The superposition of the envelope.

        Returns:
            None
        """
        
        self.basis = basis 
        self.superposition = superposition
        self.position = position
        self.radiatiion = 0
        self.lagrangian = []
        self.total_heat = 0 
    



    @property
    def hamiltonian(self):
        """
        A description of the entire function, its parameters, and its return types.
        """
        
        return self.total_heat


    def set_acceleration(self, acceleration):

        self.position.acceleration = acceleration



    def __call__(self, inertia, runners_map):

        if self.basis in [1,4,7,10]:

            basis = Derivator(domain=str(self.basis), energy=1, mass_energy=inertia, symbol=str(self.basis), runners_map= runners_map)


        elif self.basis in [2, 5, 8, 11]:

            basis = Integrator(domain=str(self.basis), energy=1, mass_energy=inertia, symbol=str(self.basis), runners_map= runners_map)
        

        elif self.basis in [3, 6, 9, 12]:

            basis = Proportional(domain=str(self.basis), energy=1, mass_energy=inertia, symbol=str(self.basis), runners_map= runners_map)

        else:

            raise ValueError('Invalid basis')

        water_earth_cardinal = self.position.element == types.Elements.WATER and self.superposition.element == types.Elements.EARTH and self.position.modality == types.Modalities.CARDINAL and self.superposition.modality == types.Modalities.CARDINAL
        earth_water_cardinal = self.position.element == types.Elements.EARTH and self.superposition.element == types.Elements.WATER and self.position.modality == types.Modalities.CARDINAL and self.superposition.modality == types.Modalities.CARDINAL
        water_earth_mFuseable = self.positionelement == types.Elements.WATER and self.sFuseABLE and self.sFuseABLE
        earth_water_mFuseable = self.position.element == types.Elements.EARTH and self.sFuseABLE and self.sFuseABLE
        water_earth_fixed = self.position.element == types.Elements.WATER and self.superposition.element == types.Elements.EARTH and self.position.modality == types.Modalities.FIXED and self.superposition.modality == types.Modalities.FIXED
        earth_water_fixed = self.position.element == types.Elements.EARTH and self.superposition.element == types.Elements.WATER and self.position.modality == types.Modalities.FIXED and self.superposition.modality == types.Modalities.FIXED
        fire_air_cardinal = self.position.element == types.Elements.FIRE and self.superposition.element == types.Elements.AIR and self.position.modality == types.Modalities.CARDINAL and self.superposition.modality == types.Modalities.CARDINAL 
        aire_fire_cardinal = self.position.element == types.Elements.AIR and self.superposition.element == types.Elements.FIRE and self.position.modality == types.Modalities.CARDINAL and self.superposition.modality == types.Modalities.CARDINAL
        fire_air_mFuseable = self.position.element == types.Elements.FIRE and self.sFuseABLE and self.sFuseABLE
        air_fire_mFuseable = self.position.element == types.Elements.AIR and self.sFuseABLE and self.sFuseABLE
        fire_air_fixed = self.position.element == types.Elements.FIRE and self.superposition.element == types.Elements.AIR and self.position.modality == types.Modalities.FIXED and self.superposition.modality == types.Modalities.FIXED
        air_fire_fixed = self.position.element == types.Elements.AIR and self.superposition.element == types.Elements.FIRE and self.position.modality == types.Modalities.FIXED and self.superposition.modality == types.Modalities.FIXED

        opposite =  water_earth_cardinal or earth_water_cardinal or water_earth_mFuseable or earth_water_mFuseable or water_earth_fixed or earth_water_fixed or fire_air_cardinal or aire_fire_cardinal or fire_air_mFuseable or air_fire_mFuseable or fire_air_fixed or air_fire_fixed

        if opposite:

            if self.position.__class__ == BiphasicOscillator:

                coeff1, coeff2 = self.position.coefficients()
                sum_a = coeff1 + coeff2

                coeff1, coeff2 = self.superposition.coefficients()
                sum_b = coeff1 + coeff2

                opposition = min(sum_a, sum_b)


                if sum_a == opposition:

                    x1, radiation = self.position(inertia)
                    self.superposition.update_coefficients(0, 0)
                    x2, radiation = self.superposition(inertia)

                
                else:

                    self.position.update_coefficients(0, 0)
                    x1, radiation = self.position(inertia)
                    x2, radiation = self.superposition(inertia)

                y = basis(x1)
                radiation = len(y) * SPEED_OF_SE
                self.radiatiion = radiation
                self.lagrangian.append(y)

                return y, radiation

            elif self.position.__class__ == TriphasicOscillator:

                coeff1, coeff2, coeff3 = self.position.coefficients()
                sum_a = coeff1 + coeff2 + coeff3

                coeff1, coeff2, coeff3 = self.superposition.coefficients()
                sum_b = coeff1 + coeff2 + coeff3

                opposed = min(sum_a, sum_b)

                if sum_a == opposed:

                    x1, radiation = self.position(inertia)
                    self.superposition.update_coefficients(0, 0, 0)
                    x2, radiation = self.superposition(inertia)
                
                else:
                    
                    self.position.update_coefficients(0, 0, 0)
                    x1, radiation = self.superposition(inertia)
                    x2, radiation = self.position(inertia)


                y = basis(x1)
                radiation = len(y) * SPEED_OF_SE
                self.radiatiion = radiation
                self.lagrangian.append(y)

                return y, radiation


            elif self.position.__class__ == QuadriphasicOscillator:

                coeff1, coeff2, coeff3, coeff4 = self.position.coefficients()
                sum_a = coeff1 + coeff2 + coeff3 + coeff4

                coeff1, coeff2, coeff3, coeff4 = self.superposition.coefficients()
                sum_b = coeff1 + coeff2 + coeff3 + coeff4

                opposed = min(sum_a, sum_b)

                if sum_a == opposed:

                    x1, radiation = self.position(inertia)
                    self.superposition.update_coefficients(0, 0, 0, 0)
                    x2, radiation = self.superposition(inertia)
                
                else:

                    self.position.update_coefficients(0, 0, 0, 0)
                    x1, radiation = self.superposition(inertia)
                    x2, radiation = self.position(inertia)

                
            
                y = basis(x1)
                radiation = len(y) * SPEED_OF_SE
                self.radiatiion = radiation
                self.lagrangian.append(y)

                return y, radiation
                
            else:

                raise ValueError('Invalid basis')


        elif self.position.name == self.superposition.name:

            if self.position.__class__ == BiphasicOscillator:

                coeff1, coeff2 = self.position.coefficients()
                sum_a = coeff1 + coeff2

                coeff1, coeff2 = self.superposition.coefficients()
                sum_b = coeff1 + coeff2

                conjuction = max(sum_a, sum_b)

                if sum_a == conjuction:

                    x1, radiation = self.position(inertia)
                    self.superposition.update_coefficients(0, 0)
                    x2, radiation = self.superposition(inertia)
                
                else:

                    self.position.update_coefficients(0, 0)
                    x1, radiation = self.superposition(inertia)
                    x2, radiation = self.position(inertia)

                y = basis(x1)
                radiation = len(y) * SPEED_OF_SE
                self.radiatiion = radiation
                self.lagrangian.append(y)

                return y, radiation

            
            elif self.position.__class__ == TriphasicOscillator:


                coeff1, coeff2, coeff3 = self.position.coefficients()
                sum_a = coeff1 + coeff2 + coeff3

                coeff1, coeff2, coeff3 = self.superposition.coefficients()
                sum_b = coeff1 + coeff2 + coeff3

                conjuction = max(sum_a, sum_b)

                if sum_a == conjuction:

                    x1, radiation = self.position(inertia)
                    self.superposition.update_coefficients(0, 0, 0)
                    x2, radiation = self.superposition(inertia)
                
                else:

                    x1, radiation = self.superposition(inertia)
                    self.position.update_coefficients(0, 0, 0)
                    x2, radiation = self.position(inertia)

                y = basis(x1)
                radiation = len(y) * SPEED_OF_SE
                self.radiatiion = radiation
                self.lagrangian.append(y)

                return y, radiation

            
            elif self.position.__class__ == QuadriphasicOscillator:

                coeff1, coeff2, coeff3, coeff4 = self.position.coefficients()
                sum_a = coeff1 + coeff2 + coeff3 + coeff4

                coeff1, coeff2, coeff3, coeff4 = self.superposition.coefficients()
                sum_b = coeff1 + coeff2 + coeff3 + coeff4

                conjuction = max(sum_a, sum_b)

                if sum_a == conjuction:

                    x1, radiation = self.position(inertia)
                    self.superposition.update_coefficients(0, 0, 0, 0)
                    x2, radiation = self.superposition(inertia)
                
                else:

                    x1, radiation = self.superposition(inertia)
                    self.position.update_coefficients(0, 0, 0, 0)
                    x2, radiation = self.position(inertia)

                y = basis(x1)
                radiation = len(y) * SPEED_OF_SE
                self.radiatiion = radiation
                self.lagrangian.append(y)


                return y, radiation
            
            else:

                raise ValueError('Invalid position')
            
  
        elif self.superposition.element == self.position.element:

            if self.position.__class__ == BiphasicOscillator:
            
                coeff1, coeff2 = self.position.coefficients()
                coeff2, coeff4 = self.superposition.coefficients()

                coff_a = coeff1 + coeff2
                coff_b = coeff2 + coeff4

                self.position.update_coefficients(coff_a, coff_b)
                self.superposition.update_coefficients(coff_a, coff_b)

                x1, radiation = self.position(inertia)
                x2, radiation = self.superposition(x1)

                y = basis(x2)
                radiation = len(y) * SPEED_OF_SE
                self.radiatiion = radiation
                self.lagrangian.append(y)

                return y, radiation
            

            elif self.position.__class__ == TriphasicOscillator:

                coeff1, coeff2, coeff3 = self.position.coefficients()
                coeff2, coeff4, coeff5 = self.superposition.coefficients()

                coff_a = coeff1 + coeff2 
                coff_b = coeff2 + coeff4
                coff_c = coeff3 + coeff5

                self.position.update_coefficients(coff_a, coff_b, coff_c)
                self.superposition.update_coefficients(coff_a, coff_b, coff_c)

                x1, radiation = self.position(inertia)
                x2, radiation = self.superposition(x1)

                y = basis(x2)
                radiation = len(y) * SPEED_OF_SE
                self.radiatiion = radiation
                self.lagrangian.append(y)

                return y, radiation


            elif self.position.__class__ == QuadriphasicOscillator:

                coeff1, coeff2, coeff3, coeff4 = self.position.coefficients()
                coeff2, coeff5, coeff6, coeff7 = self.superposition.coefficients()

                coff_a = coeff1 + coeff2
                coff_b = coeff2 + coeff5
                coff_c = coeff3 + coeff6
                coff_d = coeff4 + coeff7

                self.position.update_coefficients(coff_a, coff_b, coff_c, coff_d)
                self.superposition.update_coefficients(coff_a, coff_b, coff_c, coff_d)

                x1, radiation = self.position(inertia)
                x2, radiation = self.superposition(x1)

                y = basis(x2)
                radiation = len(y) * SPEED_OF_SE
                self.radiatiion = radiation
                self.lagrangian.append(y)

                return y, radiation
            
            else:

                raise ValueError('Invalid position')
        
        elif (self.position.element == types.Element.WATER and self.superposition.element == types.Element.EARTH) or (self.position.element == types.Element.EARTH and self.superposition.element == types.Element.WATER) or (self.position.element == types.Element.FIRE and self.position.element == types.Element.AIR) or (self.position.element == types.Element.AIR and self.superposition.element == types.Element.FIRE): 


            x1, _ = self.position(inertia)
            x2, _ = self.superposition(inertia)

            y = basis(x1, x2)
            radiation = len(y) * SPEED_OF_SE
            self.radiatiion = radiation
            self.lagrangian.append(y)

            return y, radiation


        elif self.position.modality == self.superposition.modality and self.position.element != self.superposition.element:


            if self.position.__class__ == BiphasicOscillator:
            
                coeff1, coeff2 = self.position.coefficients()
                coeff2, coeff4 = self.superposition.coefficients()

                coff_a = coeff1 - coeff2
                coff_b = coeff2 - coeff4

                if coff_a < 0: coff_a = 0
                if coff_b < 0: coff_b = 0

                self.position.update_coefficients(coff_a, coff_b)
                self.superposition.update_coefficients(coff_a, coff_b)

                x1, _ = self.position(inertia)
                x2 , _ = self.superposition(inertia)

                y = basis(x1, x2)
                radiation = len(y) * SPEED_OF_SE
                self.radiatiion = radiation
                self.lagrangian.append(y)

                return y, radiation
            

            elif self.position.__class__ == TriphasicOscillator:

                coeff1, coeff2, coeff3 = self.position.coefficients()
                coeff2, coeff4, coeff5 = self.superposition.coefficients()

                coff_a = coeff1 - coeff2
                coff_b = coeff2 - coeff4
                coff_c = coeff3 - coeff5

                if coff_a < 0: coff_a = 0
                if coff_b < 0: coff_b = 0
                if coff_c < 0: coff_c = 0

                self.position.update_coefficients(coff_a, coff_b, coff_c)
                self.superposition.update_coefficients(coff_a, coff_b, coff_c)

                x1, _ = self.position(inertia)
                x2, _ = self.superposition(inertia)

                y = basis(x1, x2)
                radiation = len(y) * SPEED_OF_SE
                self.radiatiion = radiation
                self.lagrangian.append(y)

                return y, radiation


            elif self.position.__class__ == QuadriphasicOscillator:

                coeff1, coeff2, coeff3, coeff4 = self.position.coefficients()
                coeff2, coeff5, coeff6, coeff7 = self.superposition.coefficients()

                coff_a = coeff1 - coeff2
                coff_b = coeff2 - coeff5
                coff_c = coeff3 - coeff6
                coff_d = coeff4 - coeff7

                if coff_a < 0: coff_a = 0
                if coff_b < 0: coff_b = 0
                if coff_c < 0: coff_c = 0
                if coff_d < 0: coff_d = 0

                self.position.update_coefficients(coff_a, coff_b, coff_c, coff_d)
                self.superposition.update_coefficients(coff_a, coff_b, coff_c, coff_d)

                x1, _ = self.position(inertia)
                x2, _ = self.superposition(inertia)

                y = basis(x1, x2)
                radiation = len(y) * SPEED_OF_SE
                self.radiatiion = radiation
                self.lagrangian.append(y)

                return y, radiation

            
            else:

                raise ValueError('Invalid position')
            
        
        else:

            x1, _ = self.position(inertia)
            x2, _ = self.superposition(x1)

            y = basis(x1, x2)
            radiation = len(y) * SPEED_OF_SE
            self.radiatiion = radiation
            self.lagrangian.append(y)

            return y, radiation


    @property
    def hamiltonian(self):
        """
        Returns the hamiltonian property of the object.

        :return: The hamiltonian property.
        :rtype: Any
        """
        
        return self.radiatiion


    @property
    def lagrangian(self):
        """
        Returns the lagrangian property of the object.

        :return: The lagrangian property.
        :rtype: Any
        """
        
        return self.lagrangian


    def render(self):
        """
        A description of the entire function, its parameters, and its return types.
        """
        
        formulae = f""" {self.position.formula} oo {self.basis.formula} -> {self.superposition.formula}"""

        return formulae



    def unravel(self):

        return self.basis, self.position, self.superposition





class Ensemble:

 
    def __init__(self, entity_name, basis, positions, superpositions,  runners_map) -> None:
        """
        A description of the entire function, its parameters, and its return types.
        """
        self.entity_name = entity_name
        self.techniques.append(
            self._compile(basis, positions, superpositions, runners_map)
        )

        self.lagrangian = []

   
    def add_envelopes(self, orbs, houses, pieces, runners_map):
        """
        Adds a new set of techniques to the ensemble.

        Parameters:
            orbs (list[BiphasicOscillator]): A list of BiphasicOscillator instances.
            houses (list[BiphasicOscillator]): A list of BiphasicOscillator instances.
            pieces (list[BiphasicOscillator]): A list of BiphasicOscillator instances.
            runners_map (dict): A dictionary mapping technique names to their corresponding runner functions.

        Returns:
            None
        """

        self.envelopes.append(
            self._compile(orbs, houses, pieces, runners_map)
        )

        

    @property
    def max_heat(self, heat):

        self.max_heat = heat


    @property
    def min_heat(self, heat):

        self.min_heat = heat



    def add_technique(self, orbs, houses, pieces, runners_map):
        """
        Adds a new set of techniques to the ensemble.

        Parameters:
            orbs (list[BiphasicOscillator]): A list of BiphasicOscillator instances.
            houses (list[BiphasicOscillator]): A list of BiphasicOscillator instances.
            pieces (list[BiphasicOscillator]): A list of BiphasicOscillator instances.
            runners_map (dict): A dictionary mapping technique names to their corresponding runner functions.

        Returns:
            None
        """

        new_sequence = []
        for orb, house, piece in zip(orbs, houses, pieces):

            new_sequence.append(
                (orb.name, house.name, piece.name)
            )


        exists = False #we check wether the technique already exists in a different order
        existing_sequences = []

        for ensembles in self.techniques:

            existing_sequence = []
            for env in ensembles:

                identifiers = (env.basis.name, env.position.name, env.superposition.name)

                exists = identifiers in new_sequence

                if not exists:

                     break


                existing_sequence.append(identifiers)
            

            existing_sequences.append(existing_sequence) 
            if exists == False: break

        
        if exists:

            is_different_sequence = True

            for existing_sequence in existing_sequences:

                if existing_sequence == new_sequence:

                    is_different_sequence = False
                    break

                else:

                    continue


            if is_different_sequence:

                ensemble = self._compile(orbs, houses, pieces, runners_map)

                self.techniques.append(
                    ensemble 
                )
            else:

                raise ValueError('Invalid technique')





    def render(self):
        """
        A description of the entire function, its parameters, and its return types.
        """
        
        formulae = [ env.render() + "+" for env in self.envelopes ]

        return formulae



    def collapse_envelopes(self):    

        formulae = ""
        for t in self.techniques:

            for env in t:

                formulae += env.render() + "+"

        symbols = Fuse() 
        return symbols(formulae)


    def _compile(self, orbs, houses, pieces):
        
        """
        Compile an ensemble of envelopes from a list of orbs, houses and pieces.

        Parameters:
            orbs (list[BiphasicOscillator]): A list of BiphasicOscillator instances.
            houses (list[BiphasicOscillator]): A list of BiphasicOscillator instances.
            pieces (list[BiphasicOscillator]): A list of BiphasicOscillator instances.

        Returns:
            list[Envelope]: A list of Envelope instances.
        """
        envelopes = []         

        for orb, house, piece in zip(orbs, houses, pieces):

            if orb.name == Signs.ARIES_PISCES:

                self.heat += 25

            elif orb.name == Signs.ARIES_ARIES:

                self.heat += 30

            elif orb.name == Signs.ARIES_TAURUS:

                self.heat += 20

            elif orb.name == Signs.TAURUS_ARIES:

                self.heat += 15

            elif orb.name == Signs.TAURUS_TAURUS:

                self.heat += 5

            elif orb.name == Signs.TAURUS_GEMINI:

                self.heat += 5

            elif orb.name == Signs.GEMINI_TAURUS:

                self.heat += 5

            elif orb.name == Signs.GEMINI_GEMINI:

                self.heat += 5

            elif orb.name == Signs.GEMINI_CANCER:

                self.heat += 10

            elif orb.name == Signs.CANCER_GEMINI:

                self.heat += 10


            elif orb.name == Signs.CANCER_CANCER:

                self.heat += 10


            elif orb.name == Signs.CANCER_LEO:

                self.heat += 15


            elif orb.name == Signs.LEO_CANCER:


                self.heat += 20


            elif orb.name == Signs.LEO_LEO:


                self.heat += 25


            elif orb.name == Signs.LEO_VIRGO:


                self.heat += 15


            elif orb.name == Signs.VIRGO_LEO:


                self.heat += 15


            elif orb.name == Signs.VIRGO_VIRGO:


                self.heat += 10


            elif orb.name == Signs.VIRGO_LIBRA:


                self.heat += 5


            elif orb.name == Signs.LIBRA_VIRGO:


                self.heat += 5


            elif orb.name == Signs.LIBRA_LIBRA:

                self.heat += 5


            elif orb.name == Signs.LIBRA_SCORPIO:

                self.heat -= 10


            elif orb.name == Signs.SCORPIO_LIBRA:

                self.heat -= 10


            elif orb.name == Signs.SCORPIO_SCORPIO:

                self.heat += 15


            elif orb.name == Signs.SCORPIO_SAGITTARIUS:

                self.heat += 20


            elif orb.name == Signs.SAGITTARIUS_SCORPIO:

                self.heat += 20


            elif orb.name == Signs.SAGITTARIUS_SAGITTARIUS:

                self.heat += 30


            elif orb.name == Signs.SAGITTARIUS_CAPRICORN:

                self.heat += 20


            elif orb.name == Signs.CAPRICORN_SAGITTARIUS:

                self.heat += 15

            
            elif orb.name == Signs.CAPRICORN_CAPRICORN:

                self.heat += 10

            elif orb.name == Signs.CAPRICORN_AQUARIUS:

                self.heat -= 5
            
            elif orb.name == Signs.AQUARIUS_CAPRICORN:

                self.heat += 5

            elif orb.name == Signs.AQUARIUS_AQUARIUS:

                self.heat += 10
            
            elif orb.name == Signs.AQUARIUS_PISCES:

                self.heat += 15

            elif orb.name == Signs.PISCES_AQUARIUS:

                self.heat += 5
            
            elif orb.name == Signs.PISCES_PISCES:

                self.heat += 10


            elif orb.name == Signs.PISCES_ARIES:

                self.heat += 25

            else:

                raise ValueError(f"Unrecognized orb: {orb.name}")
              


            avg = self.heat / len(orbs)

            self.max_heat = self.heat + avg
            self.min_heat = self.heat - avg

            self.envelopes.append(

                Envelope(basis = piece,
                         position=orb,
                         superposition=house)
                )
            
        return envelopes



    def reflect(self, x): 
        """
        Reflects the given input x and returns the responses.

        Parameters:
            x (float): The input to be reflected.

        Returns:
            str: The reflected input.
        """

        from random import normal

        self.hamiltonian = 0
        envelopes = self.techniques[normal(len(self.techniques), 1)]

        response = ""

        for env in envelopes:

            if env.position.element == Element.AIR or env.position.element == Element.FIRE:

                y, energy = env(x)
                heat += energy 
            
            else:

                y, potential = env(x)
                heat -= potential
            

            response += y 

        self.total_heat = heat

        if self.total_heat > self.max_heat and self.total_heat < self.min_heat: return None

        self.lagrangian.append(response)
                 
        return response, heat

    
    @property
    def lagrangian(self):
        """
        A description of the entire function, its parameters, and its return types.
        """
        
        return ''.join(self.lagrangian) 

    
    @property
    def hamiltonian(self):
        """
        A description of the entire function, its parameters, and its return types.
        """
        
        return self.total_heat

from reduce import Reduce

class Character:


    def __init__(self,
                 name,) -> None:
            

        """
        Initializes a new instance of the Character class.

        Args:
            name (str): The name of the character.
            type (str): The type of the character.

        Returns:
            None
        """

        self.name = name

   
        self.total_heat = 0
        self.charisma = 0
        self.perception = 0
        self.intelligence = 0
        self.dexterity = 0
        self.cunning = 0
        self.constitution = 0
        self.wisdom = 0
        self.strenght = 0

        self.repetition_penalty_ego = 0
        self.repetition_penalty_superego = 0
        self.repetition_penalty_shadow = 0
        self.repetition_penalty_spirit = 0


        self.has_one = False
        self.has_two = False
        self.has_three = False
        self.has_four = False
        self.has_five = False
        self.has_six = False
        self.has_seven = False
        self.has_eight = False
        self.has_nine = False
        self.has_ten = False
        self.has_eleven = False
        self.has_twelve = False




    def _map_dict_to_envelope(self, dict) -> Envelope:
        
        symbols = Fuse()
        position = symbols.by_degree_and_position(dict['pos'], dict['sign'])
        basis = symbols.by_degree_and_position(dict['name'], 0)
        superposition = symbols.by_degree_and_position(_map_to_position(dict['house']), 0)


        return Envelope(basis = basis,
                        position=position,
                        superposition=superposition)





    def fill_by_birthdate(self, birthdate, story, runners_map) -> None: 

        from kerykeion import AstrologicalSubject

        subject = AstrologicalSubject(self.name, birthdate.year, birthdate.month, birthdate.day, birthdate.hour, birthdate.city, birthdate.nation, zodiac_type='Sidereal')

        one = self._map_dict_to_envelope(subject.first_house)
        has_first = True

        two = self._map_dict_to_envelope(subject.venus)
        has_second = True

        three = self._map_dict_to_envelope(subject.mercury)
        has_third = True

        four = self._map_dict_to_envelope(subject.moon)
        has_fourth = True

        five = self._map_dict_to_envelope(subject.sun)
        has_fifth = True

        six = self._map_dict_to_envelope(subject.sixth_house)
        has_sixth = True

        seven = self._map_dict_to_envelope(subject.third_house)   
        has_seventh = True

        eight = self._map_dict_to_envelope(subject.mars)
        has_eighth = True

        nine = self._map_dict_to_envelope(subject.jupiter)
        has_ninth = True

        ten = self._map_dict_to_envelope(subject.saturn)
        has_tenth = True

        eleven = self._map_dict_to_envelope(subject.uranus)
        has_eleventh = True

        twelve = self._map_dict_to_envelope(subject.neptune)
        has_twelfth = True

        if self.has_one and self.has_two and self.has_three:

            orb_1, house_1, piece_1 = self.one.unravel()
            orb_2, house_2, piece_2 = self.two.unravel()
            orb_3, house_3, piece_3 = self.three.unravel()

            orbs = [orb_1, orb_2, orb_3]
            houses = [house_1, house_2, house_3]
            pieces = [piece_1, piece_2, piece_3]

            ensemble = Ensemble('', orbs, houses, pieces, runners_map)

            axis_filter = (AxisFilter.ego(), AxisFilter.superego(), 
                           AxisFilter.shadow(), AxisFilter.spirit())
         
            axes_rankings = [ {fi.__name__ : fi(ensemble(story))} for fi in axis_filter]
            highest_axes_spectrum = max(axes_rankings, key=lambda x: list(x.values()))

            if highest_axes_spectrum == 'EGO':

                self.ego = ensemble
                self.ego.identity = 'EGO'
            
            elif highest_axes_spectrum == 'SUPEREGO':

                self.superego = ensemble
                self.superego.identity = 'SUPEREGO'

            elif highest_axes_spectrum == 'SHADOW':

                self.shadow = ensemble
                self.shadow.identity = 'SHADOW'

            elif highest_axes_spectrum == 'SPIRIT':

                self.spirit = ensemble
                self.spirit.identity = 'SPIRIT'


        if self.has_four and self.has_five and self.has_six:

            orb_1, house_1, piece_1 = self.four.unravel()
            orb_2, house_2, piece_2 = self.five.unravel()
            orb_3, house_3, piece_3 = self.six.unravel()

            orbs = [orb_1, orb_2, orb_3]
            houses = [house_1, house_2, house_3]
            pieces = [piece_1, piece_2, piece_3]

            ensemble = Ensemble('', orbs, houses, pieces, runners_map)

            axis_filter = (AxisFilter.ego(), AxisFilter.superego(), 
                           AxisFilter.shadow(), AxisFilter.spirit())
         
            axes_rankings = [ {fi.__name__ : fi(ensemble(story))} for fi in axis_filter]
            highest_axes_spectrum = max(axes_rankings, key=lambda x: list(x.values()))

            if highest_axes_spectrum == 'SHADOW':

                self.shadow = ensemble
                self.shadow.identity = 'SHADOW'
            
            elif highest_axes_spectrum == 'SPIRIT':

                self.spirit = ensemble

            elif highest_axes_spectrum == 'EGO':

                self.ego = ensemble
                self.ego.identity = 'EGO'

            elif highest_axes_spectrum == 'SUPEREGO':

                self.superego = ensemble


        if self.has_seven and self.has_eight and self.has_nine:

            orb_1, house_1, piece_1 = self.seven.unravel()
            orb_2, house_2, piece_2 = self.eight.unravel()
            orb_3, house_3, piece_3 = self.nine.unravel()

            orbs = [orb_1, orb_2, orb_3]
            houses = [house_1, house_2, house_3]
            pieces = [piece_1, piece_2, piece_3]

            ensemble = Ensemble('', orbs, houses, pieces, runners_map)

            axis_filter = (AxisFilter.ego(), AxisFilter.superego(),
                           AxisFilter.shadow(), AxisFilter.spirit())
         
            axes_rankings = [ {fi.__name__ : fi(ensemble(story))} for fi in axis_filter]
            highest_axes_spectrum = max(axes_rankings, key=lambda x: list(x.values()))

            if highest_axes_spectrum == 'SPIRIT':

                self.spirit = ensemble
                self.spirit.identity = 'SPIRIT'

            elif highest_axes_spectrum == 'EGO':

                self.ego = ensemble
                self.ego.identity = 'EGO'

            elif highest_axes_spectrum == 'SUPEREGO':

                self.superego = ensemble
                self.superego.identity = 'SUPEREGO'

            elif highest_axes_spectrum == 'SHADOW':

                self.shadow = ensemble  
                self.shadow.identity = 'SHADOW'

        if self.has_ten and self.has_eleven and self.has_twelve:

            orb_1, house_1, piece_1 = self.ten.unravel()
            orb_2, house_2, piece_2 = self.eleven.unravel()
            orb_3, house_3, piece_3 = self.twelve.unravel()

            orbs = [orb_1, orb_2, orb_3]
            houses = [house_1, house_2, house_3]
            pieces = [piece_1, piece_2, piece_3]

            ensemble = Ensemble('', orbs, houses, pieces, runners_map)

            axis_filter = (AxisFilter.ego(), AxisFilter.superego(),
                           AxisFilter.shadow(), AxisFilter.spirit())
         
            axes_rankings = [ {fi.__name__ : fi(ensemble(story))} for fi in axis_filter]
            highest_axes_spectrum = max(axes_rankings, key=lambda x: list(x.values()))

            if highest_axes_spectrum == 'EGO':

                self.ego = ensemble
                self.ego.identity = 'EGO'

            elif highest_axes_spectrum == 'SUPEREGO':

                self.superego = ensemble
                self.superego.identity = 'SUPEREGO'

            elif highest_axes_spectrum == 'SHADOW':

                self.shadow = ensemble
                self.shadow.identity = 'SHADOW'

            elif highest_axes_spectrum == 'SPIRIT':

                self.spirit = ensemble
                self.spirit.identity = 'SPIRIT'


        if self.ego and self.spirit and self.shadow and self.superego:

            self.rest() 

            return True

        else:

            return False


    @property
    def hamiltonian(self):
        """
        A description of the entire function, its parameters, and its return types.
        """
        
        return self.ego.hamiltonian + self.superego.hamiltonian + self.shadow.hamiltonian + self.spirit.hamiltonian


    @property
    def lagrangian(self):
        """
        Calculate the Lagrangian of the object by summing the Lagrangian of its ego, superego, shadow, and spirit.

        :return: The sum of the Lagrangian of ego, superego, shadow, and spirit.
        :rtype: float
        """
      
        return self.ego.lagrangian + self.superego.lagrangian + self.shadow.lagrangian + self.spirit.lagrangian



    def reflect(self, source, turns):

        """
        Reflects the given source `turns` number of times and returns the responses.
        
        :param source: The input source for the reflection.
        :type source: Any
        :param turns: The number of turns to reflect.
        :type turns: int
        :return: A list of responses generated by the reflection process.
        :rtype: List[Any]
        """
        import inspect

        def retrieve_name(var):
            callers_local_vars = inspect.currentframe().f_back.f_locals.items()
            return [var_name for var_name, var_val in callers_local_vars if var_val is var]

        from mappers import InnerPersonalityMapper
 
        energy_a = self.ego.hamiltonian
        energy_b = self.superego.hamiltonian
        energy_c = self.shadow.hamiltonian
        energy_d = self.spirit.hamiltonian

        router = [(self.ego.hamiltonian, energy_a, self.repetition_penalty_ego), (self.superego.hamiltonian, energy_b, self.repetition_penalty_superego), (self.shadow.hamiltonian, energy_c, self.repetition_penalty_shadow), (self.spirit.hamiltonian, energy_d, self.repetition_penalty_spirit)]

        responses = [] 

        for _ in range(turns):

            switch = randint(0,1)

            if switch == 1:
            
                router.sort(key=lambda x: x[1])
            
            else:

                router.sort(key=lambda x: x[1], reverse=True)


            highest_energy_ensemble = router[0][0]
            repetition_penalty = router[0][2]

            guard = lambda: randint(0, 20)

            if guard() < repetition_penalty:

                del router[0]

                if len(router) == 0: break
                continue
            
            else:

                repetition_penalty += 1

                impulse_response, radiation = highest_energy_ensemble(source)

                sub_personality_mapper = InnerPersonalityMapper()

                if highest_energy_ensemble.identity == 'EGO':

                    impulse_response = sub_personality_mapper.ego(impulse_response)

                elif highest_energy_ensemble.identity == 'SUPEREGO':

                    impulse_response = sub_personality_mapper.superego(impulse_response)

                elif highest_energy_ensemble.identity == 'SHADOW':

                    impulse_response = sub_personality_mapper.shadow(impulse_response)

                elif highest_energy_ensemble.identity == 'SPIRIT':

                    impulse_response = sub_personality_mapper.spirit(impulse_response)

                else:

                    raise ValueError('Dimension not found.')

                

                self.total_heat += radiation

                if self.total_heat < self.min_heat or self.total_heat > self.max_heat:

                    return None
                
            

                responses.append(impulse_response)
        

        return responses

            

    def compile(self):
        

        """
        Compiles the character's attributes based on the signs of the envelopes in the ego attribute.

        Iterates over the envelopes associated with the `ego` attribute, and updates character attributes
        such as charisma, cunning, constitution, wisdom, intelligence, strength, dexterity, and perception
        according to the sign of each envelope's position. If the sign is not recognized, raises a ValueError.

        Raises:
            ValueError: If an envelope has an invalid sign.
        """
        for id_ in self.ego.envelopes.keys():

            envelope = self.ego.envelopes[id_]["envelope"]

            if envelope.position.sign == types.Signs.ARIES_PISCES:

                self.charisma += 5
                self.cunning += 5
                self.constitution += 10
                self.wisdom += 5
                self.intelligence += 5
                self.strenght += 15
                self.dexterity += 5
                self.perception += 0
                            

            elif envelope.position.sign == types.Signs.ARIES_ARIES:

                self.charisma += 5
                self.cunning += 5
                self.constitution += 10
                self.wisdom += 0
                self.intelligence += 0
                self.strenght += 15
                self.dexterity += 10
                self.perception += 5
                            

            elif envelope.position.sign == types.Signs.ARIES_TAURUS:

                self.charisma += 5
                self.cunning += 5
                self.constitution += 15
                self.wisdom += 5
                self.intelligence += 0
                self.strenght += 15
                self.dexterity += 5
                self.perception += 10
                            

            elif envelope.position.sign == types.Signs.TARUS_ARIES:

                self.charisma += 5
                self.cunning += 0
                self.constitution += 20
                self.wisdom += 10
                self.intelligence += 5
                self.strenght += 10
                self.dexterity += 5
                self.perception += 10


            elif envelope.position.sign == types.Signs.TAURUS_TAURUS:

                self.charisma += 5
                self.cunning += 0
                self.constitution += 20
                self.wisdom += 15
                self.intelligence += 10
                self.strenght += 10
                self.dexterity += 5
                self.perception += 10


            elif envelope.position.sign == types.Signs.TAURUS_GEMINI:

                self.charisma += 5
                self.cunning += 10
                self.constitution += 10
                self.wisdom += 10
                self.intelligence += 15
                self.strenght += 5
                self.dexterity += 0
                self.perception += 10

            elif envelope.position.sign == types.Signs.GEMINI_TAURUS:

                self.charisma += 10
                self.cunning += 15
                self.constitution += 5
                self.wisdom += 5
                self.intelligence += 10
                self.strenght += 5
                self.dexterity += 10
                self.perception += 10


            elif envelope.position.sign == types.Signs.GEMINI_GEMINI:

                self.charisma += 10
                self.cunning += 15
                self.constitution += 0
                self.wisdom += 5
                self.intelligence += 15
                self.strenght += 0
                self.dexterity += 15
                self.perception += 10


            elif envelope.position.sign == types.Signs.GEMINI_CANCER:

                self.charisma += 15
                self.cunning += 10
                self.constitution += 5
                self.wisdom += 10
                self.intelligence += 10
                self.strenght += 0
                self.dexterity += 10
                self.perception += 10

            elif envelope.position.sign == types.Signs.CANCER_GEMINI:

                self.charisma += 10
                self.cunning += 10
                self.constitution += 10
                self.wisdom += 10
                self.intelligence += 10
                self.strenght += 5
                self.dexterity += 5
                self.perception += 5

            elif envelope.position.sign == types.Signs.CANCER_LEO:

                self.charisma += 10
                self.cunning += 5
                self.constitution += 10
                self.wisdom += 10
                self.intelligence += 5
                self.strenght += 15
                self.dexterity += 0
                self.perception += 5

            elif envelope.position.sign == types.Signs.CANCER_CANCER:

                self.charisma += 10
                self.cunning += 5
                self.constitution += 15
                self.wisdom += 15
                self.intelligence += 5
                self.strenght += 10
                self.dexterity += 0
                self.perception += 0

            elif envelope.position.sign == types.Signs.LEO_CANCER:

                self.charisma += 15
                self.cunning += 0
                self.constitution += 10
                self.wisdom += 5
                self.intelligence += 5
                self.strenght += 15
                self.dexterity += 0
                self.perception += 0


            elif envelope.position.sign == types.Signs.LEO_LEO:

                self.charisma += 10
                self.cunning += 0
                self.constitution += 10
                self.wisdom += 5
                self.intelligence += 10
                self.strenght += 20
                self.dexterity += 0
                self.perception += 5


            elif envelope.position.sign == types.Signs.LEO_VIRGO:

                self.charisma += 5
                self.cunning += 5
                self.constitution += 10
                self.wisdom += 10
                self.intelligence += 10
                self.strenght += 15
                self.dexterity += 0
                self.perception += 0


            elif envelope.position.sign == types.Signs.VIRGO_LEO:

                self.charisma += 5
                self.cunning += 5
                self.constitution += 10
                self.wisdom += 10
                self.intelligence += 15
                self.strenght += 5
                self.dexterity += 0
                self.perception += 10


            elif envelope.position.sign == types.Signs.VIRGO_VIRGO:

                self.charisma += 5
                self.cunning += 5
                self.constitution += 5
                self.wisdom += 10
                self.intelligence += 15
                self.strenght += 5
                self.dexterity += 5
                self.perception += 15


            elif envelope.position.sign == types.Signs.VIRGO_LIBRA:

                self.charisma += 15
                self.cunning += 10
                self.constitution += 0
                self.wisdom += 5
                self.intelligence += 5
                self.strenght += 0
                self.dexterity += 10
                self.perception += 15


            elif envelope.position.sign == types.Signs.LIIBRA_VIRGO:

                self.charisma += 15
                self.cunning += 10
                self.constitution += 0
                self.wisdom += 0
                self.intelligence += 5
                self.strenght += 0
                self.dexterity += 10
                self.perception += 10


            elif envelope.position.sign == types.Signs.LIIBRA_LIBRA:

                self.charisma += 20
                self.cunning += 10
                self.constitution += 0
                self.wisdom += 0
                self.intelligence += 5
                self.strenght += 0
                self.dexterity += 15
                self.perception += 10


            elif envelope.position.sign == types.Signs.LIIBRA_SCORPIO:

                self.charisma += 15
                self.cunning += 20
                self.constitution += 5
                self.wisdom += 5
                self.intelligence += 5
                self.strenght += 5
                self.dexterity += 10
                self.perception += 15


            elif envelope.position.sign == types.Signs.SCORPIO_LIBRA:

                self.charisma += 5
                self.cunning += 10
                self.constitution += 5
                self.wisdom += 0
                self.intelligence += 5
                self.strenght += 15
                self.dexterity += 5
                self.perception += 10
            

            elif envelope.position.sign == types.Signs.SCORPIO_SCORPIO:

                self.charisma += 0
                self.cunning += 15
                self.constitution += 5
                self.wisdom += 0
                self.intelligence += 5
                self.strenght += 20
                self.dexterity += 15
                self.perception += 20


            elif envelope.position.sign == types.Signs.SCORPIO_SAGITTARIUS:

                self.charisma += 5
                self.cunning += 10
                self.constitution += 10
                self.wisdom += 5
                self.intelligence += 5
                self.strenght += 10
                self.dexterity += 20
                self.perception += 15


            elif envelope.position.sign == types.Signs.SAGITTARIUS_SCORPIO:

                self.charisma += 10
                self.cunning += 5
                self.constitution += 10
                self.wisdom += 15
                self.intelligence += 10
                self.strenght += 5
                self.dexterity += 15
                self.perception += 10


            elif envelope.position.sign == types.Signs.SAGITTARIUS_SAGITTARIUS:

                self.charisma += 10
                self.cunning += 0
                self.constitution += 10
                self.wisdom += 15
                self.intelligence += 5
                self.strenght += 10
                self.dexterity += 20
                self.perception += 10

            elif envelope.position.sign == types.Signs.SAGITTARIUS_CAPRICORN:

                self.charisma += 5
                self.cunning += 5
                self.constitution += 10
                self.wisdom += 15
                self.intelligence += 10
                self.strenght += 15
                self.dexterity += 15
                self.perception += 5

            elif envelope.position.sign == types.Signs.CAPRICORN_SAGITTARIUS:

                self.charisma += 0
                self.cunning += 5
                self.constitution += 15
                self.wisdom += 10
                self.intelligence += 15
                self.strenght += 15
                self.dexterity += 5
                self.perception += 5

            elif envelope.position.sign == types.Signs.CAPRICORN_CAPRICORN:

                self.charisma += 0
                self.cunning += 5
                self.constitution += 20
                self.wisdom += 5
                self.intelligence += 15
                self.strenght += 20
                self.dexterity += 0
                self.perception += 5


            elif envelope.position.sign == types.Signs.CAPRICORN_AQUARIUS:

                self.charisma += 5
                self.cunning += 0
                self.constitution += 10
                self.wisdom += 0
                self.intelligence += 20
                self.strenght += 15
                self.dexterity += 0
                self.perception += 5
            


            elif envelope.position.sign == types.Signs.AQUARIUS_CAPRICORN:

                self.charisma += 10
                self.cunning += 0
                self.constitution += 5
                self.wisdom += 5
                self.intelligence += 15
                self.strenght += 10
                self.dexterity += 5
                self.perception += 0
            

            elif envelope.position.sign == types.Signs.AQUARIUS_AQUARIUS:

                self.charisma += 15
                self.cunning += 0
                self.constitution += 0
                self.wisdom += 10
                self.intelligence += 20
                self.strenght += 5
                self.dexterity += 5
                self.perception += 0
            

            elif envelope.position.sign == types.Signs.AQUARIUS_PISCES:

                self.charisma += 15
                self.cunning += 5
                self.constitution += 0
                self.wisdom += 15
                self.intelligence += 15
                self.strenght += 0
                self.dexterity += 10
                self.perception += 5
            
            elif envelope.position.sign == types.Signs.PISCES_AQUARIUS:

                self.charisma += 10
                self.cunning += 10
                self.constitution += 0
                self.wisdom += 10
                self.intelligence += 15
                self.strenght += 10
                self.dexterity += 15
                self.perception += 10
            
 
            elif envelope.position.sign == types.Signs.PISCES_PISCES:

                self.charisma += 10
                self.cunning += 15
                self.constitution += 5
                self.wisdom += 15
                self.intelligence += 10
                self.strenght += 10
                self.dexterity += 15
                self.perception += 15
            

            elif envelope.position.sign == types.Signs.PISCES_ARIES:

                self.charisma += 5
                self.cunning += 15
                self.constitution += 10
                self.wisdom += 15
                self.intelligence += 10
                self.strenght += 15
                self.dexterity += 15
                self.perception += 15
            

            else:

                raise ValueError(f"Invalid sign: {envelope.position.sign}")


    def rest(self):
        """
    	Resets the repetition penalty of ego, superego, shadow, and spirit, and decreases their respective Hamiltonian values by half.
    	"""
        self.repetition_penalty_ego = 0
        self.repetition_penalty_superego = 0
        self.repetition_penalty_shadow = 0
        self.repetition_penalty_spirit = 0
        
        self.ego.hamiltonian -= int(self.ego.hamiltonian/2)
        self.superego.hamiltonian -= int(self.superego.hamiltonian/2)
        self.shadow.hamiltonian -= int(self.shadow.hamiltonian/2)
        self.spirit.hamiltonian -= int(self.spirit.hamiltonian/2)

        self.total_heat = 0
    

    def render(self):
        """
    	A description of the entire function, its parameters, and its return types.
    	"""

        summary = "\n"* 3

        for key in self.ego.envelopes.keys():

            summary += self.ego.envelopes[key]["envelope"].render()

        for key in self.superego.envelopes.keys():

            summary += self.superego.envelopes[key]["envelope"].render()

        for key in self.shadow.envelopes.keys():

            summary += self.shadow.envelopes[key]["envelope"].render()

        for key in self.spirit.envelopes.keys():

            summary += self.spirit.envelopes[key]["envelope"].render()

        return summary


    
    def anneal(self, story, runners_map):
    
        """
        Given a story, use the Reducers to generate an ensemble
        corresponding to one of the four personality axes (superego, ego,
        shadow, spirit).

        Parameters:
            story (str): a story to reflect on
            runners_map (dict): a dictionary mapping technique names to their
                corresponding runner functions

        Returns:
            bool: True if all four personality axes have been generated, False
                otherwise
        """
        
        converged = False

        while converged == False: 
    
            mapper = Map(runners_map) 
            res = mapper.text_fision(story, 1)

            ambiance, characters, house = zip(res)

            envelope = Envelope(ambiance, characters, house)

            house = house.keys()[0]


            if house == 1 and self.has_one == False:

                self.one = envelope 
                self.has_one = True
        
            elif house == 2 and self.has_two == False:

                self.two = envelope 
                self.has_two = True

            elif house == 3 and self.has_three == False:

                self.three = envelope 
                self.has_three = True

            elif house == 4 and self.has_four == False:

                self.four = envelope 
                self.has_four = True
            

            elif house == 5 and self.has_five == False:

                self.five = envelope
                self.has_five = True


            elif house == 6 and self.has_six == False:

                self.six = envelope 
                self.has_six = True


            elif house == 7 and self.has_seven == False:

                self.seven = envelope 
                self.has_seven = True

            elif house == 8 and self.has_eight == False:

                self.eight = envelope 
                self.has_eight = True

            elif house == 9 and self.has_nine == False:

                self.nine = envelope 
                self.has_nine = True

            elif house == 10 and self.has_ten == False:

                self.ten = envelope 
                self.has_ten = True

            elif house == 11 and self.has_eleven == False:

                self.eleven = envelope 
                self.has_eleven = True

            elif house == 12 and self.has_twelve == False:  

                self.twelve = envelope 
                self.has_twelve = True


            if self.has_one and self.has_two and self.has_three:

                orb_1, house_1, piece_1 = self.one.unravel()
                orb_2, house_2, piece_2 = self.two.unravel()
                orb_3, house_3, piece_3 = self.three.unravel()

                orbs = [orb_1, orb_2, orb_3]
                houses = [house_1, house_2, house_3]
                pieces = [piece_1, piece_2, piece_3]

                ensemble = Ensemble('', orbs, houses, pieces, runners_map)

                axis_filter = (AxisFilter.ego(), AxisFilter.superego(), 
                            AxisFilter.shadow(), AxisFilter.spirit())
            
                axes_rankings = [ {fi.__name__ : fi(ensemble(story))} for fi in axis_filter]
                highest_axes_spectrum = max(axes_rankings, key=lambda x: list(x.values()))

                if highest_axes_spectrum == 'EGO':

                    self.ego = ensemble
                    self.ego.identity = 'EGO'
                
                elif highest_axes_spectrum == 'SUPEREGO':

                    self.superego = ensemble
                    self.superego.identity = 'SUPEREGO'

                elif highest_axes_spectrum == 'SHADOW':

                    self.shadow = ensemble
                    self.shadow.identity = 'SHADOW'

                elif highest_axes_spectrum == 'SPIRIT':

                    self.spirit = ensemble
                    self.spirit.identity = 'SPIRIT'


            if self.has_four and self.has_five and self.has_six:

                orb_1, house_1, piece_1 = self.four.unravel()
                orb_2, house_2, piece_2 = self.five.unravel()
                orb_3, house_3, piece_3 = self.six.unravel()

                orbs = [orb_1, orb_2, orb_3]
                houses = [house_1, house_2, house_3]
                pieces = [piece_1, piece_2, piece_3]

                ensemble = Ensemble('', orbs, houses, pieces, runners_map)

                axis_filter = (AxisFilter.ego(), AxisFilter.superego(), 
                            AxisFilter.shadow(), AxisFilter.spirit())
            
                axes_rankings = [ {fi.__name__ : fi(ensemble(story))} for fi in axis_filter]
                highest_axes_spectrum = max(axes_rankings, key=lambda x: list(x.values()))

                if highest_axes_spectrum == 'SHADOW':

                    self.shadow = ensemble
                    self.shadow.identity = 'SHADOW'
                
                elif highest_axes_spectrum == 'SPIRIT':

                    self.spirit = ensemble

                elif highest_axes_spectrum == 'EGO':

                    self.ego = ensemble
                    self.ego.identity = 'EGO'

                elif highest_axes_spectrum == 'SUPEREGO':

                    self.superego = ensemble


            if self.has_seven and self.has_eight and self.has_nine:

                orb_1, house_1, piece_1 = self.seven.unravel()
                orb_2, house_2, piece_2 = self.eight.unravel()
                orb_3, house_3, piece_3 = self.nine.unravel()

                orbs = [orb_1, orb_2, orb_3]
                houses = [house_1, house_2, house_3]
                pieces = [piece_1, piece_2, piece_3]

                ensemble = Ensemble('', orbs, houses, pieces, runners_map)

                axis_filter = (AxisFilter.ego(), AxisFilter.superego(),
                            AxisFilter.shadow(), AxisFilter.spirit())
            
                axes_rankings = [ {fi.__name__ : fi(ensemble(story))} for fi in axis_filter]
                highest_axes_spectrum = max(axes_rankings, key=lambda x: list(x.values()))

                if highest_axes_spectrum == 'SPIRIT':

                    self.spirit = ensemble
                    self.spirit.identity = 'SPIRIT'

                elif highest_axes_spectrum == 'EGO':

                    self.ego = ensemble
                    self.ego.identity = 'EGO'

                elif highest_axes_spectrum == 'SUPEREGO':

                    self.superego = ensemble
                    self.superego.identity = 'SUPEREGO'

                elif highest_axes_spectrum == 'SHADOW':

                    self.shadow = ensemble  
                    self.shadow.identity = 'SHADOW'

            if self.has_ten and self.has_eleven and self.has_twelve:

                orb_1, house_1, piece_1 = self.ten.unravel()
                orb_2, house_2, piece_2 = self.eleven.unravel()
                orb_3, house_3, piece_3 = self.twelve.unravel()

                orbs = [orb_1, orb_2, orb_3]
                houses = [house_1, house_2, house_3]
                pieces = [piece_1, piece_2, piece_3]

                ensemble = Ensemble('', orbs, houses, pieces, runners_map)

                axis_filter = (AxisFilter.ego(), AxisFilter.superego(),
                            AxisFilter.shadow(), AxisFilter.spirit())
            
                axes_rankings = [ {fi.__name__ : fi(ensemble(story))} for fi in axis_filter]
                highest_axes_spectrum = max(axes_rankings, key=lambda x: list(x.values()))

                if highest_axes_spectrum == 'EGO':

                    self.ego = ensemble
                    self.ego.identity = 'EGO'

                elif highest_axes_spectrum == 'SUPEREGO':

                    self.superego = ensemble
                    self.superego.identity = 'SUPEREGO'

                elif highest_axes_spectrum == 'SHADOW':

                    self.shadow = ensemble
                    self.shadow.identity = 'SHADOW'

                elif highest_axes_spectrum == 'SPIRIT':

                    self.spirit = ensemble
                    self.spirit.identity = 'SPIRIT'


            if self.ego and self.spirit and self.shadow and self.superego:

                self.rest() 

                converged = True

            else:

                converged =  False


    def add_technique(self, ensemble, position):
        """
        Adds a new technique to one of the four personality axes (superego, ego, shadow, spirit)

        Parameters:
            ensemble (Ensemble): an ensemble of techniques to add
            position (str): the position to add the technique to (superego, ego, shadow, spirit)

        Returns:
            None
        """

        if position == 'ego':
      
            self.ego.add_new_technique(ensemble)


        elif position == 'superego':

            self.superego.add_new_technique(ensemble)


        elif position == 'shadow':

            self.shadow.add_new_technique(ensemble)


        elif position == 'spirit':

            self.spirit.add_new_technique(ensemble)

        else:

            raise ValueError(f"Invalid position: {position}")


