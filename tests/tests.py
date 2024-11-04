
from unittest import TestCase
import sys
sys.path.append('../')
import Reduce, reactor_list
import Signs
import Derivator, Integrator, Proportional



class TestOrbsNameCorrespondance(TestCase):


    def one(self):
        
        symbols = Reduce().fusion
        reactor = symbols(reactor_list[0])

        assert reactor.name == Signs.ARIES_PISCES

        reactor = symbols(reactor_list[1])

        assert reactor.name == Signs.ARIES_ARIES

        reactor = symbols(reactor_list[2])

        assert reactor.name == Signs.ARIES_TAURUS



    def two(self):

        symbols = Reduce().fusion
        reactor = symbols(reactor_list[3])

        assert reactor.name == Signs.TAURUS_Aries

        reactor = symbols(reactor_list[4])

        assert reactor.name == Signs.TAURUS_Taurus

        reactor = symbols(reactor_list[5])

        assert reactor.name == Signs.TAURUS_GEMINI


# long etc

    def three(self):

        symbols = Reduce().fusion

        reactor = symbols(reactor_list[7])

        assert reactor.name == Signs.GEMINI_Taurus

        reactor = symbols(reactor_list[8])

        assert reactor.name == Signs.GEMINI_GEMINI



    def twelve(self):

        symbols = Reduce().fusion
        reactor = symbols(reactor_list[33])

        assert reactor.name == Signs.PISCES_AQUARIUS

        reactor = symbols(reactor_list[34])

        assert reactor.name == Signs.PISCES_PISCES

        reactor = symbols(reactor_list[35])

        assert reactor.name == Signs.PISCES_ARIES



class TestEnvelopeAccelerationIsPresent(TestCase):


    def biphasic(self):
        
        symbols = Reduce().fusion
        formulae = str(5)  + reactor_list[0]
        reactor = symbols(formulae)

        assert reactor.acceleration == 5


    def triphasic(self):
        
        symbols = Reduce().fusion
        formulae = str(5)  + reactor_list[2]
        reactor = symbols(formulae)

        assert reactor.acceleration == 5


    def quadriphasic(self):
        
        symbols = Reduce().fusion
        formulae = str(5)  + reactor_list[6]
        reactor = symbols(formulae)

        assert reactor.acceleration == 5



class TestMassCoefficientsArePresent(TestCase):



    def biphasic(self):

        symbols = Reduce().fusion
        formulae = "( 2Se ~ 3Fi )" 
        reactor = symbols(formulae)

        assert reactor.coefficients == (2, 3)



    #long etc


class TestFunctionalsArePresent(TestCase):


    def biphasic(self):

        symbols = Reduce().fusion
        formulae = "( 2Se ~ 3Fi )" 
        reactor = symbols(formulae)

        assert reactor.x_main.__class__ == Derivator and reactor.x_aux.__class__ == Integrator



    def triphasic(self):

        symbols = Reduce().fusion
        formulae = "( Se ~ Fi ) oo Si"
        reactor = symbols(formulae)

        assert reactor.x_main.__class__ == Derivator and reactor.x_aux_1.__class__ == Integrator and reactor.x_aux_2.__class__ == Integrator


    def quadriphasic(self):

        symbols = Reduce().fusion
        formulae = "( Ne ~ Te ) | ( Se ~ Fe )"
        reactor = symbols(formulae)

        assert reactor.switch.__class__ == Proportional 




class TestOscillatorsArePresent(TestCase):


    def oscillator_fails():

        symbols = Reduce().fusion
        formulae = "513( 2Se ~ 3Fi )" 

        try:
            reactor = symbols(formulae)
       
        except ValueError:

            assert True

    def oscillator_succeeds():

        symbols = Reduce().fusion
        formulae = "53( 2Se ~ 3Fi )" 

        try:
            reactor = symbols(formulae)
       
        except ValueError:

           raise ValueError 

        assert True



class TestMassEnergyIsPresent(TestCase):


    def biphasic(self):

        symbols = Reduce().fusion
        formulae = "( 2Se ~ 3Fi )" 
        reactor = symbols(formulae, me_1='Hi', me_2='Hi')

        assert reactor.x_aux.mass_energy == 'Hi' and reactor.x_main.mass_energy == 'Hi'



    def triphasic(self):

        symbols = Reduce().fusion
        formulae = "( Se ~ Fi ) oo Si"
        reactor = symbols(formulae, me_1='Hi', me_2='Hi', me_3='Hi')

        assert reactor.x_aux_2.mass_energy == 'Hi' and reactor.x_aux_1.mass_energy == 'Hi' and reactor.x_main.mass_energy == 'Hi'



    def quadriphasic(self):

        symbols = Reduce().fusion
        formulae = "( Ne ~ Te ) | ( Se ~ Fe )"
        reactor = symbols(formulae, me_1='Hi', me_2='Hi', me_3='Hi', me_4='Hi')

        assert reactor.x1.x_main == 'Hi' and reactor.x1.x_aux.mass_energy == 'Hi' and reactor.x2.x_main.mass_energy == 'Hi' and reactor.x2.x_main.mass_energy == 'Hi' and reactor.x2.x_aux.mass_energy == 'Hi'





from filters import Rerankers
from mappers import FunctionMapper
from util.runners import TextRunner

class FunctionalTests(TestCase):


    def Te(self):

        identity, prompt  = Rerankers().rerank()
        runner = TextRunner()

        runners_map = {"N": 'medium', "S": 'medium', "T": 'medium', "F": 'medium'}


        Te = Derivator(
            domain="T",
            energy=5,
            mass_energy="I'm trying to organize.",
            runners_map=runners_map,
            symbol="Te",
        )

        response = Te("Hi, how are you?")

        db = FunctionMapper()

        prompt.format(specification=db.te(),

        behavior=response)

        score = runner(identity, prompt)

        assert score['hallucination'] < 30 == True
        assert score['releavance'] > 60 == True



    def Ne(self):

        identity, prompt  = Rerankers().rerank()
        runner = TextRunner()

        runners_map = {"N": 'medium', "S": 'medium', "T": 'medium', "F": 'medium'}


        Ne = Derivator(
            domain="N",
            energy=5,
            mass_energy="I'm trying to imagine something else.",
            runners_map=runners_map,
            symbol="Ne",
        )


        response = Ne("Hi, how are you?")

        db = FunctionMapper()

        prompt.format(specification=db.ne(),

        behavior=response)

        score = runner(identity, prompt)

        assert score['releavance'] < 30 == True
        assert score['hallucination'] > 60 == True 


    def Ti_joint_Se(self):

        identity, prompt  = Rerankers().rerank()

        runners_map = {"N": 'medium', "S": 'medium', "T": 'medium', "F": 'medium'}

        runner = TextRunner()
        Ti = Integrator(
            domain="T",
            potential=5,
            mass_energy="I'm trying to think a solution.",
            runners_map=runners_map,
            symbol="Ti",
        )

        Se = Derivator(
           domain="S",
           energy=5,
           mass_energy="I'm trying to do something.",
           runners_map=runners_map,
           symbol="Se",
       )
       

        response = Ti(Se("Hi, how are you?"))

        db = FunctionMapper()

        prompt.format(specification=db.ti_se(),

        behavior=response)

        score = runner(identity, prompt)

        assert score['releavance'] < 30 == True
        assert score['hallucination'] > 60 == True



    def Ni_joint_Ti(self):

        identity, prompt  = Rerankers().rerank()

        runners_map = {"N": 'medium', "S": 'medium', "T": 'medium', "F": 'medium'}

        runner = TextRunner()
        Ni = Integrator(
            domain="N",
            potential=5,
            mass_energy="I'm trying to think a solution.",
            runners_map=runners_map,
            symbol="Ni",
        )

        Ti = Integrator(
           domain="T",
           potential=5,
           mass_energy="I'm trying to do something.",
           runners_map=runners_map,
           symbol="Ti",
       )
       

        response = Ni(Ti("Hi, how are you?"))

        db = FunctionMapper()

        prompt.format(specification=db.ni_ti(),

        behavior=response)

        score = runner(identity, prompt)

        assert score['releavance'] < 30 == True
        assert score['hallucination'] > 60 == True 



    def Sn(self):

        identity, prompt  = Rerankers().rerank()
        runner = TextRunner()

        runners_map = {"N": 'medium', "S": 'medium', "T": 'medium', "F": 'medium'}


        Sn = Proportional(
            domain="S",
            energy=5,
            potential=5,
            runners_map=runners_map,
        ) 

        Ni = Integrator(
            domain="N",
            potential=5,
            mass_energy="I'm trying to think a solution.",
            runners_map=runners_map,
            symbol="Ni",
        )

        Ti = Integrator(
           domain="T",
           potential=5,
           mass_energy="I'm trying to do something.",
           runners_map=runners_map,
           symbol="Ti",
       )
       

        response_1 = Ni(Ti("Hi, how are you?"))


        Te = Derivator(
           domain="T",
           energy=5,
           mass_energy="I'm trying to do something.",
           runners_map=runners_map,
           symbol="Te",
       )
        
        Se = Derivator(
            domain="S",
            energy=5,
            mass_energy="I'm trying to do something.",
            runners_map=runners_map,
            symbol="Se",
        )

        response_2 = Te(Se("Hi, how are you?"))


        response = Sn(response_1 + response_2)

        db = FunctionMapper()

        prompt.format(specification=db.sn(),

        behavior=response)

        score = runner(identity, prompt)

        assert score['releavance'] < 30 == True
        assert score['hallucination'] > 60 == True



from containers import Envelope




class EnvelopesTests(TestCase):




    def sample(self):

        envelope = Envelope()
        runner = TextRunner()
        runners_map = {"N": 'medium', "S": 'medium', "T": 'medium', "F": 'medium'}

        symbols = Reduce()
        oscillator = symbols.fuse("( Se ~ Fe ) oo Si", me_1='Hi', me_2='Hi', me_3='Hi')

        #should only be able to be sampled once

        try:

            response_a = oscillator("Hi, how are you?", 1)

        except  ValueError:
    
            assert False

        assert True



    def exhaustion(self):

        envelope = Envelope()
        runner = TextRunner()
        runners_map = {"N": 'medium', "S": 'medium', "T": 'medium', "F": 'medium'}

        symbols = Reduce()
        oscillator = symbols.fuse("2( Se ~ Fe ) oo Si", me_1='Hi', me_2='Hi', me_3='Hi')

        #should only be able to be sampled once

        response_a = oscillator("Hi, how are you?", 2)

        try:

            response_b = oscillator("And then what else?", 1)

        except  ValueError:
    
            assert True


from containers import Ensemble

class EnsembleTests(TestCase):
    

    
    def add_heat(self):
        
        runners_map = {"N": 'medium', "S": 'medium', "T": 'medium', "F": 'medium'}
        symbols = Reduce()
        oscillator = symbols.fuse("(Se ~ Fe) oo Si", me_1='Hi', me_2='Hi', me_3='Hi')
        ensemble = Ensemble(oscillator)

        #should only be able to be sampled once

        assert ensemble.heat == 25 
    


    def add_heat_then_cold(self):

        symbols = Reduce()

        runners_map = {"N": 'medium', "S": 'medium', "T": 'medium', "F": 'medium'}

        oscillator_a = symbols.fuse("(Se ~ Fe) oo Si", me_1='Hi', me_2='Hi', me_3='Hi')
        oscillator_b = symbols.fuse("(Se oo Si)", me_1='Hi', me_2='Hi')
        oscillator_c = symbols.by_degree_and_position('Sco', 5)

        basis_a, positions_a, superpositions_a = oscillator_a.unravel()
        basis_b, positions_b, superpositions_b = oscillator_b.unravel()
        basis_c, positions_c, superpositions_c = oscillator_c.unravel()

        ensemble = Ensemble( [basis_a, basis_b, basis_c], [positions_a, positions_b, positions_c], [superpositions_a, superpositions_b, superpositions_c], runners_map)

        assert ensemble.heat == 10

    

    def exhaustion(self):

        runners_map = {"N": 'medium', "S": 'medium', "T": 'medium', "F": 'medium'}
        symbols = Reduce()
        oscillator = symbols.fuse("(Se ~ Fe) oo Si", me_1='Hi', me_2='Hi', me_3='Hi')
        ensemble = Ensemble(oscillator)

        try:

            ensemble.reflect("How are you?")

            assert True

        except  ValueError:

            assert False


        try:

            ensemble.reflect("How are you?")

            assert False

        except  ValueError:

            assert True



    def render(self): 
        
        symbols = Reduce()

        runners_map = {"N": 'medium', "S": 'medium', "T": 'medium', "F": 'medium'}

        oscillator_a = symbols.fuse("(Se ~ Fe) oo Si", me_1='Hi', me_2='Hi', me_3='Hi')
        oscillator_b = symbols.fuse("(Se oo Si)", me_1='Hi', me_2='Hi')
        oscillator_c = symbols.by_degree_and_position('Sco', 5)

        basis_a, positions_a, superpositions_a = oscillator_a.unravel()
        basis_b, positions_b, superpositions_b = oscillator_b.unravel()
        basis_c, positions_c, superpositions_c = oscillator_c.unravel()

        ensemble = Ensemble( [basis_a, basis_b, basis_c], [positions_a, positions_b, positions_c], [superpositions_a, superpositions_b, superpositions_c], runners_map)

        assert ensemble.render() == '(Se ~ Fe) oo Si + (Se oo Si) +  (Se -> Ni) ~ Fe'
 

from containers import Character
import pytest


class CharactersTests(TestCase):

    def test_initialization_default_attributes(self):

        character = Character(name="Test Character")
        assert character.total_heat == 0
        assert character.charisma == 0
        assert character.perception == 0
        assert character.intelligence == 0
        assert character.dexterity == 0
        assert character.cunning == 0
        assert character.constitution == 0
        assert character.wisdom == 0
        assert character.strenght == 0
        assert character.repetition_penalty_ego == 0
        assert character.repetition_penalty_superego == 0
        assert character.repetition_penalty_shadow == 0
        assert character.repetition_penalty_spirit == 0


    def test_compile_invalid_sign_raises_value_error(self, mocker):

        character = Character(name="Test Character")
        mock_envelope = mocker.Mock()
        mock_envelope.position.sign = "INVALID_SIGN"
        character.ego = mocker.Mock()
        character.ego.envelopes = {"1": {"envelope": mock_envelope}}
    
        with pytest.raises(ValueError, match="Invalid sign: INVALID_SIGN"):
            character.compile()


    def test_fill_by_birthdate_correct_mapping(self, mocker):
        from datetime import datetime
        from kerykeion import AstrologicalSubject
        from reaper.containers import Character

        # Mock AstrologicalSubject to control its behavior
        mock_subject = mocker.patch('kerykeion.AstrologicalSubject', autospec=True)
        mock_subject.return_value.first_house = {'pos': 1, 'sign': 'Aries', 'name': 'First House'}
        mock_subject.return_value.venus = {'pos': 2, 'sign': 'Taurus', 'name': 'Venus'}
        mock_subject.return_value.mercury = {'pos': 3, 'sign': 'Gemini', 'name': 'Mercury'}
        # ... continue mocking other attributes as needed

        character = Character(name="Test Character")
        birthdate = datetime(1990, 1, 1, 12, 0)
        story = "Test Story"
        runners_map = {}

        result = character.fill_by_birthdate(birthdate, story, runners_map)

        assert result is True
        assert character.ego is not None
        assert character.spirit is not None
        assert character.shadow is not None
        assert character.superego is not None

    def test_fill_by_birthdate_invalid_input(self, mocker):
        from reaper.containers import Character

        # Mock AstrologicalSubject to raise an exception for invalid input
        mocker.patch('kerykeion.AstrologicalSubject', side_effect=ValueError("Invalid birthdate"))

        character = Character(name="Test Character")
        birthdate = "invalid_date"  # Invalid birthdate format
        story = "Test Story"
        runners_map = {}

        try:
            result = character.fill_by_birthdate(birthdate, story, runners_map)
            assert result is False
        except ValueError as e:
            assert str(e) == "Invalid birthdate"


    def test_router_empty_handling(self, mocker):
        # Mocking necessary components
        mock_ego = mocker.Mock()
        mock_superego = mocker.Mock()
        mock_shadow = mocker.Mock()
        mock_spirit = mocker.Mock()
    
        # Setting high repetition penalties to ensure router becomes empty
        character = Character()
        character.ego = mock_ego
        character.superego = mock_superego
        character.shadow = mock_shadow
        character.spirit = mock_spirit
        character.repetition_penalty_ego = 20
        character.repetition_penalty_superego = 20
        character.repetition_penalty_shadow = 20
        character.repetition_penalty_spirit = 20
    
        # Testing reflect method with high penalties
        result = character.reflect('source', 3)
    
        # Asserting that the result is an empty list due to router being empty
        assert result == []


    def test_reflect_correct_turns(self, mocker):

        # Mocking necessary components
        mock_ego = mocker.Mock()
        mock_superego = mocker.Mock()
        mock_shadow = mocker.Mock()
        mock_spirit = mocker.Mock()
        mock_ego.hamiltonian.return_value = ('response_ego', 5)
        mock_superego.hamiltonian.return_value = ('response_superego', 5)
        mock_shadow.hamiltonian.return_value = ('response_shadow', 5)
        mock_spirit.hamiltonian.return_value = ('response_spirit', 5)
    
        # Mocking InnerPersonalityMapper
        mock_mapper = mocker.patch('mappers.InnerPersonalityMapper', autospec=True)
        mock_mapper_instance = mock_mapper.return_value
        mock_mapper_instance.ego.return_value = 'mapped_ego'
        mock_mapper_instance.superego.return_value = 'mapped_superego'
        mock_mapper_instance.shadow.return_value = 'mapped_shadow'
        mock_mapper_instance.spirit.return_value = 'mapped_spirit'
    
        # Creating an instance of the class containing reflect method
        character = Character()
        character.ego = mock_ego
        character.superego = mock_superego
        character.shadow = mock_shadow
        character.spirit = mock_spirit
        character.min_heat = 0
        character.max_heat = 100
    
        # Testing reflect method
        result = character.reflect('source', 3)
    
        # Asserting the expected responses
        assert result == ['mapped_ego', 'mapped_superego', 'mapped_shadow']



    def test_compile_valid_signs(self):

        from reaper.containers import Character
        from reaper.util import types

        character = Character()
        character.ego.envelopes = {
            1: {"envelope": types.Element(position=types.Modality(sign=types.Signs.ARIES_PISCES))}
        }
    
        character.compile()
    
        assert character.charisma == 5
        assert character.cunning == 5
        assert character.constitution == 10
        assert character.wisdom == 5
        assert character.intelligence == 5
        assert character.strenght == 15
        assert character.dexterity == 5
        assert character.perception == 0
    

    def test_compile_invalid_sign_raises_value_error(self):

        from reaper.containers import Character
        from reaper.util import types

        character = Character()
        character.ego.envelopes = {
            1: {"envelope": types.Element(position=types.Modality(sign="INVALID_SIGN"))}
        }
    
        with pytest.raises(ValueError, match="Invalid sign: INVALID_SIGN"):
            character.compile()
        


        # Adding a technique to the 'ego' axis successfully updates the ego attribute
    def test_add_technique_to_ego(self, mocker):
        # Arrange
        character = Character()
        ensemble = mocker.Mock()
        character.ego = mocker.Mock()
    
        # Act
        character.add_technique(ensemble, 'ego')
    
        # Assert
        character.ego.add_new_technique.assert_called_once_with(ensemble)


        # Providing an invalid position raises a ValueError
    def test_add_technique_invalid_position(self, mocker):
        # Arrange
        character = Character()
        ensemble = mocker.Mock()
    
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid position: invalid"):
            character.add_technique(ensemble, 'invalid')
    

from filter import OrbFilter, HouseFilter, PieceFilter

class FilterTest(TestCase):
        

    def test_orb_filter(self):
        
        runner = TextRunner()
        orbs = OrbFilter()

        identity, prompt, _ = orbs.two()

        prompt.format(
            document="Hello, how are you?"
        )

        result = runner(identity, prompt)

        assert result.isdigit() == True


    def test_house_filter(self):
        
        runner = TextRunner()
        house = HouseFilter()

        identity, prompt, _ = house.two()

        prompt.format(
            document="Hello, how are you?"
        )

        result = runner(identity, prompt)

        assert result.isdigit() == True


    def test_piece_filter(self):
        
        runner = TextRunner()
        pieces = PieceFilter()

        identity, prompt, _ = pieces.two()

        prompt.format(
            document="Hello, how are you?"
        )

        result = runner(identity, prompt)

        assert result.isdigit() == True



class FisionTtest(TestCase):

    def test_generate_ensemble_of_text_techniques(self, mocker):
        # Arrange
        mock_runner = mocker.Mock()
        mock_runner.return_value = "mocked_analysis"
        mock_runners_map = {'high': mock_runner, 'low': mock_runner}
        document = "Sample document text."
        ensemble_size = 3
        text_fision_instance = Reduce()
        text_fision_instance.runners_map = mock_runners_map

        # Act
        result = text_fision_instance.text_fision(document, ensemble_size)

        # Assert
        assert isinstance(result, Ensemble)
        assert len(result.techniques) > 0


    def test_handle_empty_document(self, mocker):
        # Arrange
        mock_runner = mocker.Mock()
        mock_runner.return_value = "mocked_analysis"
        mock_runners_map = {'high': mock_runner, 'low': mock_runner}
        document = ""
        ensemble_size = 3
        text_fision_instance = Reduce()
        text_fision_instance.runners_map = mock_runners_map

        # Act
        result = text_fision_instance.text_fision(document, ensemble_size)

        # Assert
        assert isinstance(result, Ensemble)
        assert len(result.techniques) == 0




        # test the convolutions and filters aswell
    def test_text_fision_convolutions_and_filters(self, mocker):

        from map import Map
        # Mock the runners_map and its methods
        mock_runners_map = {
            'high': mocker.Mock(return_value="Mocked Analysis"),
            'low': mocker.Mock(return_value={'dim': 2, 'formula': 'mock_formula', 'acceleration': 1})
        }

        # Mock the Reduce class and its fusion method
        mock_fusion = mocker.patch('reaper.reduce.Reduce.fusion', return_value='Mocked Fusion')

        # Create an instance of the class containing text_fision
        instance = Map()
        instance.runners_map = mock_runners_map

        # Call the method under test
        document = "Sample document text"
        ensemble_size = 3
        result = instance.text_fision(document, ensemble_size)

        # Assert that the result is an instance of Ensemble
        assert isinstance(result, Ensemble)

        # Assert that the fusion method was called
        assert mock_fusion.called