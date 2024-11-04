from map import Integrator, Derivator, Proportional
from containers import Envelope, Technique, Ensemble
from util.runners import RAG, TextRunner 
from util.context_mapppers import map_coefficient_to_ctx_size, map_coefficient_to_rag_k
from mappers import BiphasicOscillator, TriphasicOscillator, QuadriphasicOscillator
from parsers import parse_formulae
from util.identifiers import Elements, Modalities, Signs, AngularMomentumOperators
from parsers import parse_formulae
from util.identifiers import Elements, Modalities, Signs
import re


class IllegalOperationError(Exception):
    pass

class FuseUtil:

    def opposite_domain(self,dimension):
        opposites = {'N': 'S', 'S': 'N', 'F': 'T', 'T': 'F'}
        return opposites[dimension]


    # Parsing functions and terms
    def parse_term(self,term):

        match = re.match(r'(\d*)\(([^)]+)\)', term)

        if match:
            acceleration = int(match.group(1)) if match.group(1) else 1
            inside = match.group(2)
            return acceleration, inside
        return 1, term

    def parse_function(self, func):
        match = re.match(r'(\d*)([A-Z][a-z])', func)
        if match:
            coefficient = int(match.group(1)) if match.group(1) else 1
            function = match.group(2)
            return coefficient, function
        return 1, func

    # Define operator functions
    def handle_oo(self, left, right):
        coeff_l, func_l = left
        coeff_r, func_r = right
        if func_l[1] == func_r[1] and func_l != func_r:
            if coeff_l > coeff_r:
                return coeff_l - coeff_r, f"{func_l} → {self.opposite_domain(func_r)}"
            elif coeff_r > coeff_l:
                return coeff_r - coeff_l, f"{func_r} → {self.opposite_domain(func_l)}"
            else:
                return 1, f"{self.opposite_domain(func_l)} → {func_r}"
        return coeff_l, func_l

    def handle_drag(left, right):
        coeff_l, func_l = left
        coeff_r, func_r = right
        if coeff_l >= coeff_r:
            return coeff_l - coeff_r, f"{func_l} → {func_r}"
        else:
            return coeff_r - coeff_l, f"{func_r} → {func_l}"

    def handle_orbital(left, right):
        coeff_l, func_l = left
        coeff_r, func_r = right
        if (func_l[0] in ['N', 'S'] and func_r[0] in ['T', 'F']) or (func_l[0] in ['T', 'F'] and func_r[0] in ['N', 'S']):
            return coeff_l, f"{func_l} ~ {func_r}"
        else:
            raise IllegalOperationError(f"Illegal orbit between {func_l} and {func_r}")

    # Function to reduce terms, with priority rules
    def reduce_terms(self, terms):
        reduced_term = []
        incompatible_terms = []

        total_acceleration = 0

        for term in terms:
            acceleration, inside = self.parse_term(term.strip())
            total_acceleration += acceleration
            functions = re.split(r'([~→oo|])', inside)

            i = 0
            term_stack = []

            while i < len(functions):
                if functions[i] in ['~', '→', 'oo']:
                    operator = functions[i]
                    left = self.parse_function(functions[i - 1])
                    right = self.parse_function(functions[i + 1])

                    if operator == '~':
                        result = self.handle_orbital(left, right)
                    elif operator == '→':
                        result = self.handle_drag(left, right)
                    elif operator == 'oo':
                        result = self.handle_oo(left, right)

                    term_stack.append(result)
                    i += 2
                else:
                    func = self.parse_function(functions[i])
                    term_stack.append(func)
                    i += 1

            # Combine term results into a single string and check for incompatibility
            final_term = term_stack[0]
            for j in range(1, len(term_stack)):
                coeff, func = term_stack[j]
                if func != final_term[1]:
                    # If the dimensions are incompatible, push to separate set
                    if func[0] != final_term[1][0]:
                        incompatible_terms.append(f"{coeff}{func}")
                    else:
                        final_term = (final_term[0] + coeff, final_term[1])

            reduced_term.append(f"{final_term[0]}{final_term[1]}")

        return total_acceleration, reduced_term, incompatible_terms



class Fuser:


    def __init__(self):
        self.util = FuseUtil()


    def fuse(self, expression):
        """
        Fuses a given expression into a specific oscillator based on its ground state and coefficients.

        Args:
            expression (str): The input expression to be processed and used for the creation of oscillators.

        Returns:
            str: The fuses expression.

        Raises:
            IllegalOperationError: If the calculated acceleration exceeds the predefined SPEED_OF_SE.

        """
        pass

        terms = expression.split('+')
        total_acceleration, reduced_term, incompatible_terms = self.util.reduce_terms(terms)

        if incompatible_terms:
            
            for i, term in enumerate(incompatible_terms):
                try:
                    reduced_accel, reduced_incompatible, _ = self.util.reduce_terms([term])
                    incompatible_terms[i] = ' '.join(reduced_incompatible)
                except IllegalOperationError:
                    continue
            
            return f"{total_acceleration}({ ' ~ '.join(reduced_term)} | {' ~ '.join(incompatible_terms)})"
        
        return f"{total_acceleration}({ ' ~ '.join(reduced_term)})"


reactor_list = [

    "( Se ~ Fi )",
    "( Se oo Si )",
    "( Se ~ Fi ) oo Si",
    "( Si  ~ Fe ) oo Se",
    "( Si oo Se )",
    "( Ne - > Si ) ~ Fe",
    "( Ne ~ Te ) | ( Se ~ Fe )",
    "( Ne ~ Fe )",
    "( Ne ~ Ti ) | ( Se ~ Fi )",
    "( Ne ~ Fi ) | ( Se ~ Ti )",
    "( Fe oo Fi )",
    "( Fi oo Fe ) ~ Si",
    "( Fi -> Te ) ~ Se ",
    "( Te ~ Ni )",
    "( Te ~ Se ) | ( Fe ~ Ne )",
    "( Si ~ Te ) | ( Ni ~ Fe )",
    "Si ~ ( Te oo Ti )",
    "(Si ~ Fe) | (Ni ~ Te)",
    "( Fe ~ Si | Te ~ Ni )",
    "( Fi oo Fe )",
    "( Fe oo Fi ) ~ Ni",
    "( Se -> Ni ) ~ Fe",
    "( Ni -> Se )",
    "( Se ~ Fi ) | ( Ne ~ Ti )",
    "Ni ~ ( Te -> Fi )",
    "( Se ~ Te ) | ( Ne ~ Fe )",
    "( Se ~ Ti )",
    "( Ne ~ Ti ) | ( Se ~ Fi)",
    "( Te oo Ti )",
    "( Ti oo Te ) ~ Ni",
    "Fi -> ( Te oo Ti )",
    "( Fe -> Ti ) ~ Ne",
    "( Ti ~ Ne ) | ( Fi ~ Se )",
    "( Fi ~ Se ) | ( Ti ~ Ne )",
    "( Ne ~ Fi ) | ( Se ~ Ti )",
    "( Fi ~ Ne | Ti ~ Se )"
]



SPEED_OF_SE = 512


class Reduce:


    def fusion(self, formula, runners_map, **kwargs):
        
        """
        Fuses a given formula into a specific oscillator based on its ground state and coefficients.

        Args:
            formula (str): The input formula to be processed and used for the creation of oscillators.
            runners_map (dict): A mapping used in the creation of derivatives and integrators.
            **kwargs: Additional keyword arguments to specify mass energies and other parameters.

        Returns:
            Oscillator: An instance of either BiphasicOscillator, TriphasicOscillator, or QuadriphasicOscillator 
                        based on the provided formula's ground state.

        Raises:
            ValueError: If the calculated acceleration exceeds the predefined SPEED_OF_SE.
        """
        import re

        def format_expression(expression):
            # Step 1: Remove all whitespaces
            expression_no_whitespace = re.sub(r'\s+', '', expression)
            
            # Step 2: Add spaces around specific operators (oo, →, |, ~)
            expression_formatted = re.sub(r'(oo|→|\||~)', r' \1 ', expression_no_whitespace)
            
            # Step 3: Remove extra spaces introduced at the edges if any
            expression_formatted = expression_formatted.strip()
            
            return expression_formatted

        formula = format_expression(formula)

        ground_state, coefficients, operators, accelerators = parse_formulae(formula)

        if len(accelerators) == 1: acceleration = accelerators[0] 
        acceleration = accelerators[0] 
        me_1 = kwargs.get('me_1', '')
        me_2 = kwargs.get('me_2', '')

        local = kwargs.get('local', True)

        if acceleration > SPEED_OF_SE: raise ValueError('Acceleration cannot be greater than the speed of Se.')

        rank = acceleration 

        for coff in coefficients: rank *= coff


        if ground_state == '(Se ~ Fi)':

            Se = Derivator(domain='S', energy = coefficients[0], mass_energy=me_1, symbol='Se', runners_map=runners_map)
            Fi = Integrator(domain='F', potential = coefficients[1], mass_energy = me_2, symbol='Fi', runners_map=runners_map)

            return BiphasicOscillator(formula = formula, 
                                      ground_state=ground_state, 
                                      x_main = Fi, 
                                      x_aux = Se, 
                                      acceleration=acceleration,
                                      operators = operators, 
                                      name=Signs.ARIES_PISCES, 
                                      element=Elements.FIRE, 
                                      modality=Modalities.CARDINAL,
                                      rank=rank,
                                      local=local,
                                      switch=True,
                                      )


        elif ground_state == '(Se oo Si)':

            Se = Derivator(domain='S', energy = coefficients[0], mass_energy=me_1, symbol='Se', runners_map=runners_map)
            Si = Integrator(domain='S', potential = coefficients[1], mass_energy = me_2, symbol='Si', runners_map=runners_map)

            return BiphasicOscillator(formula = formula, 
                                      ground_state=ground_state, 
                                      x_aux = Si, 
                                      x_main = Se, 
                                      acceleration = acceleration, 
                                      operators = operators, 
                                      name=Signs.ARIES_ARIES, 
                                      element=Elements.FIRE, 
                                      modality=Modalities.CARDINAL,
                                      rank=rank,
                                      local=local,
                                      )
        

        elif ground_state == '(Se ~ Fi) oo Si':
        
            me_3 = kwargs.get('me_3', '')

            Se = Derivator(domain='S', energy = coefficients[0], mass_energy=me_1, symbol='Se', runners_map=runners_map)
            Fi = Integrator(domain='F', potential = coefficients[1], mass_energy = me_2, symbol='Fi', runners_map=runners_map)
            Si = Integrator(domain='S', potential = coefficients[2], mass_energy = me_3, symbol='Si', runners_map=runners_map)

            return TriphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x_main = Se,
                                        x_aux_1 = Fi,
                                        x_aux_2 = Si, 
                                        acceleration = acceleration, 
                                        operators = operators, 
                                        name=Signs.ARIES_PISCES, 
                                        element=Elements.FIRE, 
                                        modality=Modalities.CARDINAL,
                                        rank=rank,
                                        local=local,
                                        )

          


        elif ground_state == '(Si ~ Fe) oo Se':

            me_3 = kwargs.get('me_3', '')

            Si = Integrator(domain='S', potential = coefficients[0], mass_energy  = me_1, symbol='Si', runners_map=runners_map)
            Fe = Derivator(domain='F', potential = coefficients[1], mass_energy  = me_2, symbol='Fe', runners_map=runners_map)
            Se = Derivator(domain='S', energy = coefficients[2],     mass_energy =me_3, symbol='Se', runners_map=runners_map)   

            return TriphasicOscillator(formula = formula,
                                      ground_state=ground_state,
                                      x_main = Si,
                                      x_aux_1 = Fe,
                                      x_aux_2 = Se,
                                      acceleration = acceleration,
                                      operators = operators,
                                      name=Signs.TAURUS_ARIES,
                                      element=Elements.EARTH,
                                      modality=Modalities.FIXED,
                                      rank=rank,
                                      local=local,
                                      )


        elif ground_state == '(Si oo Se)':

        
            Si = Integrator(domain='S', potential = coefficients[0], mass_energy = me_1, symbol='Si', runners_map=runners_map)
            Se = Derivator(domain='S', energy = coefficients[1],    mass_energy=me_2, symbol='Se', runners_map=runners_map)
           
            return BiphasicOscillator(formula = formula,
                                      ground_state=ground_state, 
                                      x_main = Se, 
                                      x_aux = Si, 
                                      acceleration = acceleration, 
                                      operators = operators, 
                                      name=Signs.TAURUS_ARIES, 
                                      element=Elements.EARTH, 
                                      modality=Modalities.FIXED,
                                      rank=rank,
                                      local=local,
                                      )



        elif ground_state == '(Ne -> Si) ~ Fe':

            me_3 = kwargs.get('me_3', '')

            Ne = Derivator(domain='N', energy = coefficients[0],     mass_energy=me_1, symbol='Ne', runners_map=runners_map)
            Si = Integrator(domain='S', potential = coefficients[1], mass_energy = me_2, symbol='Si', runners_map=runners_map)
            Fe = Derivator(domain='F', potential = coefficients[2], mass_energy = me_3, symbol='Fe', runners_map=runners_map)

            return TriphasicOscillator(formula = formula,
                                      ground_state=ground_state,
                                      x_main = Ne,
                                      x_aux_1 = Si,
                                      x_aux_2 = Fe,
                                      acceleration= acceleration,
                                      operators = operators,
                                      name=Signs.TAURUS_TAURUS,
                                      element=Elements.EARTH,
                                      modality=Modalities.FIXED,
                                      rank=rank,
                                      local=local,
                                      )


        elif ground_state == '(Ne ~ Te) | (Se ~ Fe)': 

            me_3 = kwargs.get('me_3', '')
            me_4 = kwargs.get('me_4', '')

            Ne = Derivator(domain='N', energy = coefficients[0], mass_energy=me_1, symbol='Ne', runners_map=runners_map)
            Te = Derivator(domain='T', energy = coefficients[1], mass_energy=me_2, symbol='Te', runners_map=runners_map)
            Se = Derivator(domain='S', energy = coefficients[2], mass_energy=me_3, symbol='Se', runners_map=runners_map)
            Fe = Derivator(domain='F', energy = coefficients[3], mass_energy=me_4, symbol='Fe', runners_map=runners_map)

            l_energy = coefficients[0] + coefficients[1] 
            r_potential = coefficients[2] + coefficients[3] 

            switch = Proportional(domain='NS', energy=l_energy, potential=r_potential)

            return QuadriphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x1 = Ne, 
                                        y1 = Te, 
                                        x2 = Se, 
                                        y2 = Fe, 
                                        acceleration=  acceleration, 
                                        operators = operators, 
                                        name=Signs.GEMINI_TAURUS, 
                                        element=Elements.AIR, 
                                        modality=Modalities.MU,
                                        rank=rank,
                                        switch=switch,
                                        first_composed=True,
                                        local=local,
                                        )


        elif ground_state == '(Ne ~ Fe)':


            Ne = Derivator(domain='N', energy = coefficients[0], mass_energy=me_1, symbol='Ne', runners_map=runners_map)
            Fe = Derivator(domain='F', energy = coefficients[1], mass_energy=me_2,  symbol='Fe', runners_map=runners_map)

            return BiphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x_aux = Fe, 
                                        x_main = Ne, 
                                        acceleration = acceleration, 
                                        operators = operators, 
                                        name=Signs.GEMINI_GEMINI, 
                                        element=Elements.AIR, 
                                        modality=Modalities.MU,
                                        rank=rank,
                                        local=local,
                                        )



        elif ground_state == '(Ne ~ Ti) | (Se ~ Fi)':

            me_3 = kwargs.get('me_3', '')
            me_4 = kwargs.get('me_4', '')

            Ne = Derivator(domain='N', energy = coefficients[0],     mass_energy=me_1, symbol='Ne', runners_map=runners_map)
            Ti = Integrator(domain='T', potential = coefficients[1], mass_energy = me_2, symbol='Ti', runners_map=runners_map)
            Se = Derivator(domain='S', energy = coefficients[2],     mass_energy=me_3, symbol='Se', runners_map=runners_map)
            Fi = Integrator(domain='F', potential = coefficients[3], mass_energy = me_4, symbol='Fi', runners_map=runners_map)

            l_energy = coefficients[0] + coefficients[1]
            r_potential = coefficients[2] + coefficients[3]

            switch = Proportional(domain='NS', energy=l_energy, potential=r_potential)

            return QuadriphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x1 = Ne, 
                                        y1 = Ti, 
                                        x2 = Se, 
                                        y2 = Fi, 
                                        acceleration=  acceleration, 
                                        operators = operators, 
                                        name=Signs.GEMINI_CANCER, 
                                        element=Elements.AIR, 
                                        modality=Modalities.MU,
                                        rank=rank,
                                        switch=switch,
                                        first_composed=True, 
                                        local=local,
                                        )


        elif ground_state == '(Ne ~ Fi) | (Se ~ Ti)':  

            me_3 = kwargs.get('me_3', '')
            me_4 = kwargs.get('me_4', '')

            Ne = Derivator(domain='N', energy = coefficients[0], mass_energy=me_1, symbol='Ne', runners_map=runners_map)
            Fi = Integrator(domain='F', potential = coefficients[1], mass_energy = me_2, symbol='Fi', runners_map=runners_map)
            Se = Derivator(domain='S', energy = coefficients[2], mass_energy=me_3, symbol='Se', runners_map=runners_map)
            Ti = Integrator(domain='T', potential = coefficients[3], mass_energy = me_4, symbol='Ti', runners_map=runners_map)

            l_energy = coefficients[0] + coefficients[1]
            r_potential = coefficients[2] + coefficients[3]

            switch = Proportional(domain='NS', energy=l_energy, potential=r_potential)

            return QuadriphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x1 = Ne, 
                                        y1 = Fi, 
                                        x2 = Se, 
                                        y2 = Ti, 
                                        acceleration = acceleration,
                                        operators = operators,
                                        name=Signs.CANCER_GEMINI, 
                                        element=Elements.WATER, 
                                        modality=Modalities.CARDINAL,
                                        rank=rank,
                                        switch=switch,
                                        first_composed=True,
                                        local=local,
                                        )


        elif ground_state == '(Fe oo Fi)':
            
            Fe = Derivator(domain='F', energy = coefficients[0], mass_energy=me_1, symbol='Fe', runners_map=runners_map)
            Fi = Integrator(domain='F', potential = coefficients[1], mass_energy = me_2, symbol='Fi', runners_map=runners_map)

            return BiphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x_aux = Fe, 
                                        x_main = Fi, 
                                        frequency = acceleration, 
                                        operators = operators, 
                                        name=Signs.CANCER_CANCER, 
                                        element=Elements.WATER, 
                                        modality=Modalities.CARDINAL,
                                        rank=rank,
                                        local=local,
                                       )


        elif ground_state == '(Fi oo Fe) ~ Si':

            me_3 = kwargs.get('me_3', '')

            Fi = Integrator(domain='F', potential = coefficients[0], mass_energy = me_1, symbol='Fi', runners_map=runners_map)  
            Fe = Derivator(domain='F', energy = coefficients[1], mass_energy=me_2, symbol='Fe', runners_map=runners_map)
            Si = Integrator(domain='S', potential = coefficients[2], mass_energy = me_3, symbol='Si', runners_map=runners_map)

            return TriphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x_main = Fe, 
                                        x_aux_1=  Fi, 
                                        x_aux_2 = Si, 
                                        acceleration = acceleration, 
                                        operators = operators, 
                                        name=Signs.CANCER_LEO, 
                                        element=Elements.WATER, 
                                        modality=Modalities.CARDINAL,
                                        rank=rank,
                                        local=local,
                                       )


        elif ground_state == '(Fi -> Te) ~ Se':

            me_3 = kwargs.get('me_3', '')

            Fi = Integrator(domain='F', potential = coefficients[0], mass_energy = me_1, symbol='Fi', runners_map=runners_map)
            Te = Derivator(domain='T', energy = coefficients[1], mass_energy = me_2, symbol='Te', runners_map=runners_map)
            Se = Derivator(domain='S', energy = coefficients[2], mass_energy = me_3, symbol='Se', runners_map=runners_map)

            return TriphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x_main = Fi, 
                                        x_aux_1=  Te, 
                                        x_aux_2 = Se, 
                                        acceleration= acceleration, 
                                        operators = operators, 
                                        name=Signs.LEO_CANCER, 
                                        element=Elements.FIRE, 
                                        modality=Modalities.FIXED,
                                        rank=rank,
                                        local=local,
                                      )

        elif ground_state == '(Te ~ Ni)':

            Te = Derivator(domain='T', energy = coefficients[0], mass_energy =me_1, symbol='Te', runners_map=runners_map)
            Ni = Integrator(domain='N', potential = coefficients[1], mass_energy = me_2, symbol='Ni', runners_map=runners_map)

            return BiphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x_aux = Ni, 
                                        x_main = Te, 
                                        acceleration = acceleration, 
                                        operators = operators, 
                                        name=Signs.LEO_LEO, 
                                        element=Elements.FIRE, 
                                        modality=Modalities.FIXED,
                                        rank=rank,
                                        local=local,
                                        )



        elif ground_state == '(Te ~ Se) | (Fe ~ Ne)':

            me_3 = kwargs.get('me_3', '')
            me_4 = kwargs.get('me_4', '')

            Te = Derivator(domain='T', energy = coefficients[0], mass_energy=me_1, symbol='Te' ,runners_map=runners_map)
            Se = Derivator(domain='S', energy = coefficients[1], mass_energy=me_2, symbol='Se' ,runners_map=runners_map)
            Fe = Derivator(domain='F', energy = coefficients[2], mass_energy=me_3, symbol='Fe' ,runners_map=runners_map)
            Ne = Derivator(domain='N', energy = coefficients[3], mass_energy=me_4, symbol='Ne' ,runners_map=runners_map)

            l_energy = coefficients[0] + coefficients[1] 
            r_potential = coefficients[2] + coefficients[3] 

            switch = Proportional(domain='TF', energy = l_energy, potential = r_potential)

            return QuadriphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x1 = Te, 
                                        y1 = Se, 
                                        x2 = Fe, 
                                        y2 = Ne, 
                                        acceleration = acceleration, 
                                        operators = operators, 
                                        name=Signs.LEO_VIRGO, 
                                        element=Elements.FIRE, 
                                        modality=Modalities.FIXED,
                                        rank=rank,
                                        switch=switch,
                                        local=local,
                                        )


        elif ground_state == '(Si ~ Te) | (Ni ~ Fe)':

            me_3 = kwargs.get('me_3', '')
            me_4 = kwargs.get('me_4', '')

            Si = Integrator(domain='S', potential = coefficients[0], mass_energy = me_1, symbol='Si', runners_map=runners_map)
            Te = Derivator(domain='T', energy = coefficients[1], mass_energy=me_2, symbol='Te', runners_map=runners_map) 
            Ni = Integrator(domain='N', potential = coefficients[2], mass_energy = me_3, symbol='Ni', runners_map=runners_map)
            Fe = Derivator(domain='F', energy = coefficients[3], mass_energy=me_4, symbol='Fe', runners_map=runners_map)
            
            l_hamiltonian = coefficients[0] + coefficients[1]
            r_hamiltonian = coefficients[2] + coefficients[3]

            switch = Proportional(domain='SN', energy = l_hamiltonian, potential = r_hamiltonian)

            return QuadriphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x1 = Si, 
                                        y1 = Te, 
                                        x2 = Ni, 
                                        y2 = Fe, 
                                        acceleration = acceleration, 
                                        operators = operators, 
                                        name=Signs.VIRGO_LEO, 
                                        element=Elements.EARTH, 
                                        modality=Modalities.MU,
                                        rank=rank,
                                        switch=switch,
                                        local=local,
                                      )


        elif ground_state == 'Si ~ (Te oo Ti)':

            me_3 = kwargs.get('me_3', '')

            Si = Integrator(domain='S', potential = coefficients[0], mass_energy = me_1, symbol='Si', runners_map=runners_map)
            Te = Derivator(domain='T', energy = coefficients[1], mass_energy=me_2, symbol='Te', runners_map=runners_map)
            Ti = Integrator(domain='T', potential = coefficients[2], mass_energy = me_3, symbol='Ti', runners_map=runners_map)

            return TriphasicOscillator(formula = formula,
                                        ground_state=ground_state, 
                                        x_main = Si, 
                                        x_aux_1 = Te, 
                                        x_aux_2=  Ti, 
                                        acceleration = acceleration, 
                                        operators = operators, 
                                        name=Signs.VIRGO_VIRGO, 
                                        element=Elements.EARTH, 
                                        modality=Modalities.MU,
                                        rank=rank,
                                        local=local,
                                        type2=True,
                                        )    


        elif ground_state == '(Si ~ Fe) | (Ni ~ Te)':

            me_3 = kwargs.get('me_3', '')
            me_4 = kwargs.get('me_4', '')

            Si = Integrator(domain='S', potential = coefficients[0], mass_energy = me_1, symbol='Si', runners_map=runners_map)
            Fe = Derivator(domain='F', energy = coefficients[1], mass_energy=me_2, symbol='Fe', runners_map=runners_map)

            Ni = Integrator(domain='N', potential = coefficients[2], mass_energy = me_3, symbol='Ni', runners_map=runners_map)
            Te = Derivator(domain='T', energy = coefficients[3], mass_energy=me_4, symbol='Te', runners_map=runners_map)

            l_hamiltonian = coefficients[0] + coefficients[1]
            r_hamiltonian = coefficients[2] + coefficients[3]

            switch = Proportional(domain='SN', energy = l_hamiltonian, potential = r_hamiltonian)

            return QuadriphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x1 = Si, 
                                        y1 = Fe, 
                                        x2 = Ni, 
                                        y2 = Te, 
                                        acceleration = acceleration, 
                                        operators = operators, 
                                        name=Signs.VIRGO_LIBRA, 
                                        element=Elements.EARTH, 
                                        modality=Modalities.MU,
                                        rank=rank,
                                        switch=switch,
                                        local=local,
                                       )



        elif ground_state == '(Fe ~ Si | Te ~ Ni)':

            me_3 = kwargs.get('me_3', '')
            me_4 = kwargs.get('me_4', '')

            Fe = Derivator(domain='F', potential = coefficients[0], mass_energy = me_1, symbol='Fe', runners_map=runners_map)
            Si = Integrator(domain='S', energy = coefficients[1], mass_energy=me_2, symbol='Si', runners_map=runners_map)

            Te = Derivator(domain='T', potential = coefficients[2], mass_energy = me_3, symbol='Te', runners_map=runners_map)
            Ni = Integrator(domain='N', energy = coefficients[3], mass_energy=me_4, symbol='Ni', runners_map=runners_map)


            l_hamiltonian = coefficients[0] + coefficients[1]
            r_hamiltonian = coefficients[2] + coefficients[3]

            switch = Proportional(domain='FT', energy = l_hamiltonian, potential = r_hamiltonian)

            return QuadriphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x1 = Si, 
                                        y1 = Fe, 
                                        x2 = Te, 
                                        y2 = Ni, 
                                        acceleration = acceleration, 
                                        operators = operators, 
                                        name=Signs.LIBRA_VIRGO, 
                                        element=Elements.AIR, 
                                        modality=Modalities.CARDINAL,
                                        rank=rank,
                                        switch=switch,
                                        local=local,
                                        ) 
                                       
        elif ground_state == '(Fi oo Fe)':
            
            Fi = Integrator(domain='F', potential = coefficients[0], mass_energy = me_1, symbol='Fi', runners_map=runners_map)
            Fe = Derivator(domain='F', potential = coefficients[1], mass_energy = me_2, symbol='Fe', runners_map=runners_map)

            return BiphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x_main = Fi, 
                                        x_aux = Fe, 
                                        acceleration = acceleration, 
                                        operators = operators, 
                                        name=Signs.LIBRA_LIBRA, 
                                        element=Elements.AIR, 
                                        modality=Modalities.CARDINAL,
                                        rank=rank,
                                        local=local,
                                        )


        elif ground_state == '(Fe oo Fi) ~ Ni':
            
            me_3 = kwargs.get('me_3', '')

            Fe = Derivator(domain='F', energy = coefficients[0], mass_energy=me_1, symbol='Fe', runners_map=runners_map)
            Fi = Integrator(domain='F', potential = coefficients[1], mass_energy = me_2, symbol='Fi', runners_map=runners_map)
            Ni = Integrator(domain='N', potential = coefficients[2], mass_energy = me_3, symbol='Ni', runners_map=runners_map)

            return TriphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x_main = Fe, 
                                        x_aux_1 = Fi, 
                                        x_aux_2 = Ni, 
                                        acceleration = acceleration, 
                                        operators = operators, 
                                        name=Signs.LIBRA_SCORPIO, 
                                        element=Elements.AIR,
                                        modality=Modalities.CARDINAL,
                                        rank=rank,
                                        local=local,
                                        )



        elif ground_state == '(Se -> Ni) ~ Fe':

            me_3 = kwargs.get('me_3', '')

            Se = Derivator(domain='S', energy = coefficients[0], mass_energy=me_1, symbol='Se', runners_map=runners_map)
            Ni = Integrator(domain='N', potential = coefficients[1], mass_energy = me_2, symbol='Ni', runners_map=runners_map)
            Fe = Derivator(domain='F', energy = coefficients[2], mass_energy=me_3, symbol='Fe', runners_map=runners_map)


            return TriphasicOscillator(formula = formula,
                                        ground_state=ground_state, 
                                        x_main = Se, 
                                        x_aux_1 = Ni, 
                                        x_aux_2 = Fe, 
                                        frequency = acceleration, 
                                        operators = operators, 
                                        name=Signs.SCORPIO_LIBRA, 
                                        element=Elements.WATER, 
                                        modality=Modalities.FIXED,
                                        rank=rank,
                                        local=local,
                                        )



        elif ground_state == '(Ni -> Se)':

            Ni = Integrator(domain='N', potential = coefficients[0], mass_energy = me_1, symbol='Ni', runners_map=runners_map)
            Se = Derivator(domain='S', energy = coefficients[1], mass_energy=me_2, symbol='Se', runners_map=runners_map)

            return BiphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x_aux = Se, 
                                        x_main = Ni, 
                                        acceleration = acceleration, 
                                        operators = operators, 
                                        name=Signs.SCORPIO_SCORPIO, 
                                        element=Elements.WATER, 
                                        modality=Modalities.FIXED,
                                        rank=rank,
                                        local=local,
                                        )


        elif ground_state == "(Se ~ Fi) | (Ne ~ Ti)":

            me_3 = kwargs.get('me_3', '')
            me_4 = kwargs.get('me_4', '')

            Se = Derivator(domain='S', energy = coefficients[0], mass_energy=me_1, symbol='Se', runners_map=runners_map)
            Fi = Integrator(domain='F', potential = coefficients[1], mass_energy = me_2, symbol='Fi', runners_map=runners_map)
            Ne = Derivator(domain='N', energy = coefficients[2], mass_energy=me_3, symbol='Ne', runners_map=runners_map)
            Ti = Integrator(domain='T', potential = coefficients[3], mass_energy = me_4, symbol='Ti', runners_map=runners_map)
            
            l_hamiltonian = coefficients[0] + coefficients[1]
            r_hamiltonian = coefficients[2] + coefficients[3]

            switch = Proportional(domain='SN', energy = l_hamiltonian, potential=r_hamiltonian)


            return QuadriphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x1 = Fi, 
                                        y1 = Se, 
                                        x2 = Ti, 
                                        y2 = Ne, 
                                        acceleration= acceleration, 
                                        operators = operators, 
                                        name=Signs.SCORPIO_SAGITTARIUS, 
                                        element=Elements.WATER, 
                                        modality=Modalities.FIXED,
                                        rank=rank,
                                        switch=switch,
                                        local=local,
                                        )


        elif ground_state == "Ni ~ (Te -> Fi)":

            me_3 = kwargs.get('me_3', '')

            Ni = Integrator(domain='N', potential = coefficients[0], mass_energy = me_1, symbol='Ni', runners_map=runners_map)
            Te = Derivator(domain='T', energy = coefficients[1], mass_energy=me_2, symbol='Te', runners_map=runners_map)
            Fi = Integrator(domain='F', potential = coefficients[2], mass_energy = me_3, symbol='Fi', runners_map=runners_map)

            return TriphasicOscillator(formula = formula,
                                        ground_state=ground_state, 
                                        x_main = Ni, 
                                        x_aux_1 = Te, 
                                        x_aux_2 = Fi, 
                                        acceleration = acceleration, 
                                        operators = operators, 
                                        name=Signs.SAGITTARIUS_SCORPIO, 
                                        element=Elements.FIRE, 
                                        modality=Modalities.MU,
                                        rank=rank,
                                        local=local,
                                        type2=True,
                                        )



        elif ground_state == "(Se ~ Te) | (Ne ~ Fe)":

            me_2 = kwargs.get('me_2', '')
            me_3 = kwargs.get('me_3', '')
            me_4 = kwargs.get('me_4', '')

            Se = Derivator(domain='S', energy = coefficients[0], mass_energy=me_1, symbol='Se', runners_map=runners_map)
            Te = Derivator(domain='T', energy = coefficients[1], mass_energy=me_2, symbol='Te', runners_map=runners_map)
            Ne = Derivator(domain='N', energy = coefficients[2], mass_energy=me_3, symbol='Ne', runners_map=runners_map)
            Fe = Derivator(domain='F', energy = coefficients[3], mass_energy=me_4, symbol='Fe', runners_map=runners_map)


            left_energy = coefficients[0] + coefficients[1]
            right_energy = coefficients[2] + coefficients[3]

            switch = Proportional(domain='SN', energy = left_energy, potential=right_energy)

            return QuadriphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x1 = Te, 
                                        y1 = Se, 
                                        x2 = Fe, 
                                        y2 = Ne, 
                                        acceleration = acceleration, 
                                        operators = operators, 
                                        name=Signs.SAGITTARIUS_SAGITTARIUS, 
                                        element=Elements.FIRE, 
                                        modality=Modalities.MU,
                                        rank=rank,
                                        switch=switch,
                                        local=local,
                                        )


        elif ground_state == '(Se ~ Ti)':


            Se = Derivator(domain='S', energy = coefficients[0], mass_energy=me_1, symbol='Se', runners_map=runners_map)
            Ti = Integrator(domain='T', potential = coefficients[1], mass_energy  = me_2, symbol='Ti', runners_map=runners_map)

            return BiphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x_aux = Ti, 
                                        x_main = Se, 
                                        acceleration= acceleration, 
                                        operators = operators, 
                                        name=Signs.SAGITTARIUS_CAPRICORN, 
                                        element=Elements.FIRE, 
                                        modality=Modalities.MU,
                                        rank=rank,
                                        local=local,
                                        )


        elif ground_state == '(Ne ~ Ti) | (Se ~ Fi)':

            me_3 = kwargs.get('me_3', '')
            me_4 = kwargs.get('me_4', '')

            Ne = Derivator(domain='N', energy = coefficients[0], mass_energy=me_1, symbol='Ne', runners_map=runners_map)
            Ti = Integrator(domain='T', potential = coefficients[1], mass_energy = me_2, symbol='Ti',   runners_map=runners_map)
            Se = Derivator(domain='S', energy = coefficients[2], mass_energy= me_3, symbol='Se', runners_map=runners_map)
            Fi = Integrator(domain='F', potential = coefficients[3], mass_energy = me_4, symbol='Fi', runners_map=runners_map)
            
            l_hamiltonian = coefficients[0] + coefficients[1]
            r_hamiltonian = coefficients[2] + coefficients[3]

            switch = Proportional(domain='NS', energy = l_hamiltonian, potential=r_hamiltonian)

            return QuadriphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x1 = Ti, 
                                        y1 = Ne, 
                                        x2 = Fi, 
                                        y2 = Se, 
                                        acceleration = acceleration, 
                                        operators = operators, 
                                        name=Signs.CAPRICORN_SAGITTARIUS, 
                                        element=Elements.EARTH, 
                                        modality=Modalities.CARDINAL,
                                        rank=rank,
                                        switch=switch,
                                        local=local,
                                        )


        elif ground_state == '(Te oo Ti)':

            Te = Derivator(domain='T', energy = coefficients[0], mass_energy=me_1, symbol='Te', runners_map=runners_map)
            Ti = Integrator(domain='T', potential = coefficients[1], mass_energy = me_2, symbol='Ti', runners_map=runners_map)

            return BiphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x_aux = Ti, 
                                        x_main = Te, 
                                        acceleration = acceleration, 
                                        operators = operators, 
                                        name=Signs.CAPRICORN_CAPRICORN, 
                                        element=Elements.EARTH, 
                                        modality=Modalities.CARDINAL,
                                        rank=rank,
                                        local=local,
                                        )


        elif ground_state == '(Ti oo Te) ~ Ni':


            me_3 = kwargs.get('me_3', '')

            Ti = Integrator(domain='T', potential = coefficients[0], mass_energy = me_1, symbol='Ti', runners_map=runners_map)
            Te = Derivator(domain='T', energy = coefficients[1], mass_energy=me_2, symbol='Te', runners_map=runners_map)
            Ni = Integrator(domain='N', potential = coefficients[2], mass_energy = me_3, symbol='Ni', runners_map=runners_map)

            return TriphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x_main=Ti,
                                        x_aux_1=Te,
                                        x_aux_2=Ni,
                                        acceleration = acceleration, 
                                        operators = operators, 
                                        name=Signs.CAPRICORN_AQUARIUS, 
                                        element=Elements.EARTH, 
                                        modality=Modalities.CARDINAL,
                                        rank=rank,
                                        local=local,
                                        )
        

        elif ground_state == 'Fi -> (Te oo Ti)':

            me_3 = kwargs.get('me_3', '')

            Fi = Integrator(domain='F', potential = coefficients[0], mass_energy = me_1, symbol='Fi', runners_map=runners_map)
            Te = Derivator(domain='T', energy = coefficients[1], mass_energy=me_2, symbol='Te', runners_map=runners_map)
            Ti = Integrator(domain='T', potential = coefficients[2], mass_energy = me_3, symbol='Ti', runners_map=runners_map)

            return TriphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x_main=Fi,
                                        x_aux_1=Te,
                                        x_aux_2=Ti,
                                        acceleration = acceleration, 
                                        operators = operators, 
                                        name=Signs.AQUARIUS_CAPRICORN, 
                                        element=Elements.AIR, 
                                        modality=Modalities.FIXED,
                                        rank=rank,
                                        local=local,
                                        type2=True,
                                        )


        elif ground_state == '(Fe -> Ti) ~ Ne':
            
            me_3 = kwargs.get('me_3', '')  

            Fe  = Derivator(domain='F', energy = coefficients[0], mass_energy=me_1, symbol='Fe', runners_map=runners_map)
            Ti = Integrator(domain='T', potential = coefficients[1], mass_energy = me_2, symbol='Ti', runners_map=runners_map)
            Ne = Derivator(domain='N', energy = coefficients[2], mass_energy = me_3, symbol='Ne', runners_map=runners_map)

            return TriphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x_main=Fe,
                                        x_aux_1=Ti,
                                        x_aux_2=Ne,
                                        acceleration = acceleration, 
                                        operators = operators, 
                                        name=Signs.AQUARIUS_AQUARIUS, 
                                        element=Elements.AIR, 
                                        modality=Modalities.FIXED,
                                        rank=rank,
                                        local=local
                                        )


        elif ground_state == '(Ti ~ Ne) | (Fi ~ Se)':

            me_3 = kwargs.get('me_3', '')
            me_4 = kwargs.get('me_4', '')

            Ti = Integrator(domain='T', potential = coefficients[0], mass_energy = me_1, symbol='Ti', runners_map=runners_map)
            Ne = Derivator(domain='N', energy = coefficients[1], mass_energy= me_2, symbol='Ne', runners_map=runners_map)
            Fi = Integrator(domain='F', potential = coefficients[2], mass_energy = me_3, symbol='Fi', runners_map=runners_map)
            Se = Derivator(domain='S', energy = coefficients[3], mass_energy=me_4, symbol='Se', runners_map=runners_map)


            l_hamiltonian = coefficients[0] + coefficients[1]
            r_hamiltonian = coefficients[2] + coefficients[3]

            switch = Proportional(domain='TF', energy=l_hamiltonian, potential=r_hamiltonian)
        

            return QuadriphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x1 = Ne, 
                                        y1 = Ti, 
                                        x2 = Se, 
                                        y2 = Fi, 
                                        acceleration = acceleration, 
                                        operators = operators, 
                                        name=Signs.AQUARIUS_PISCES, 
                                        element=Elements.AIR, 
                                        modality=Modalities.FIXED,
                                        rank=rank,
                                        switch=switch,
                                        local=local,
                                        )


        elif ground_state == '(Fi ~ Se) | (Ti ~ Ne)':

            me_3 = kwargs.get('me_3', '')
            me_4 = kwargs.get('me_4', '')

            Fi = Integrator(domain='F', potential = coefficients[0], mass_energy = me_1, symbol='Fi', runners_map=runners_map)
            Se = Derivator(domain='S', energy = coefficients[1], mass_energy=me_2, symbol='Se', runners_map=runners_map)
            Ti = Integrator(domain='T', potential = coefficients[2], mass_energy = me_3, symbol='Ti', runners_map=runners_map)
            Ne = Derivator(domain='N', energy = coefficients[3], mass_energy=me_4, symbol='Ne', runners_map=runners_map)

            l_hamiltonian = coefficients[0] + coefficients[1]
            r_hamiltonian = coefficients[2] + coefficients[3]

            switch = Proportional(domain='FT', energy=l_hamiltonian, potential=r_hamiltonian)

            return QuadriphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x1 = Fi, 
                                        y1 = Se, 
                                        x2 = Ne, 
                                        y2 = Ti, 
                                        acceleration= acceleration, 
                                        operators = operators,
                                        name=Signs.PISCES_AQUARIUS,
                                        element=Elements.WATER, 
                                        modality=Modalities.MU,
                                        rank=rank,
                                        switch=switch,
                                        local=local,
                                        )


        elif ground_state == '(Ne ~ Fi) | (Se ~ Ti)':

            me_3 = kwargs.get('me_3', '')
            me_4 = kwargs.get('me_4', '')

            Ne = Derivator(domain='N', energy = coefficients[0], mass_energy=me_1, symbol='Ne', runners_map=runners_map)
            Fi = Integrator(domain='F', potential = coefficients[1], mass_energy = me_2, symbol='Fi', runners_map=runners_map)

            Se = Derivator(domain='S', energy = coefficients[2], mass_energy=me_3, symbol='Se', runners_map=runners_map)
            Ti = Integrator(domain='T', potential = coefficients[3], mass_energy = me_4, symbol='Ti', runners_map=runners_map)

            left_hamiltonian = coefficients[0] + coefficients[2]
            right_hamiltonian = coefficients[1] + coefficients[3]

            switch = Proportional(domain='NS', energy= left_hamiltonian, potential= right_hamiltonian)


            return QuadriphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x1 = Ti, 
                                        y1 = Ne, 
                                        x2 = Fi,
                                        y2 = Se, 
                                        acceleration = acceleration, 
                                        operators = operators,
                                        name=Signs.PISCES_PISCES,
                                        element=Elements.WATER, 
                                        modality=Modalities.MU,
                                        rank=rank,
                                        switch=switch,
                                        local=local,
                                        )
   

        elif ground_state == '(Ne ~ Ti) | (Se ~ Fi)':

            me_3 = kwargs.get('me_3', '')
            me_4 = kwargs.get('me_4', '')

            Ne = Derivator(domain='N', energy = coefficients[0], mass_energy=me_1, symbol='Ne', runners_map=runners_map)
            Ti = Integrator(domain='T', potential = coefficients[1], mass_energy = me_2, symbol='Ti', runners_map=runners_map)

            Se = Derivator(domain='S', energy = coefficients[2], mass_energy = me_3, symbol='Se', runners_map=runners_map)
            Fi = Integrator(domain='F', potential = coefficients[3], mass_energy = me_4, symbol='Fi', runners_map=runners_map)

            left_hamiltonian = coefficients[0] + coefficients[2]
            right_hamiltonian = coefficients[1] + coefficients[3]

            switch = Proportional(domain='NS', energy= left_hamiltonian, potential= right_hamiltonian)


            return QuadriphasicOscillator(formula = formula, 
                                        ground_state=ground_state, 
                                        x1 = Ti, 
                                        y1 = Ne, 
                                        x2 = Fi,
                                        y2 = Se, 
                                        acceleration= acceleration, 
                                        operators = operators,
                                        name=Signs.PISCES_ARIES,
                                        element=Elements.WATER, 
                                        modality=Modalities.MU,
                                        rank=rank,
                                        switch=switch,  
                                        local=local,
                                        )


        else:


            oscillator = self.fuse(formula)

            return oscillator 

    def by_degree_and_position(self, degree, position):
        
        if position == 'Ars' or position == 'Aries' and degree >= 0 and degree <= 10:

            self.__call__(reactor_list[0])

        
        elif position == 'Ars' or position == 'Aries' and degree >= 11 and degree <= 20:

            self.__call__(reactor_list[1])

        
        elif position == 'Ars' or position == 'Aries' and degree >= 21 and degree <= 30:

            self.__call__(reactor_list[2])



        elif position == 'Tau' or position == 'Taurus' and degree >= 0 and degree <= 10:

            self.__call__(reactor_list[3])


        elif position == 'Tau' or position == 'Taurus' and degree >= 11 and degree <= 20:

            self.__call__(reactor_list[4])

        elif position == 'Tau' or position == 'Taurus' and degree >= 21 and degree <= 30:

            self.__call__(reactor_list[5])


        elif position == 'Gem' or position == 'Gemini' and degree >= 0 and degree <= 10:

            self.__call__(reactor_list[6])


        elif position == 'Gem' or position == 'Gemini' and degree >= 11 and degree <= 20:

            self.__call__(reactor_list[7])


        elif position == 'Gem' or position == 'Gemini' and degree >= 21 and degree <= 30:

            self.__call__(reactor_list[8])


        elif position == 'Can' or position == 'Cancer' and degree >= 0 and degree <= 10:

            self.__call__(reactor_list[9])
    

        elif position == 'Can' or position == 'Cancer' and degree >= 11 and degree <= 20:

            self.__call__(reactor_list[10])


        elif position == 'Can' or position == 'Cancer' and degree >= 21 and degree <= 30:

            self.__call__(reactor_list[11])


        elif position == 'Leo' or position == 'Leo'  and degree >= 0 and degree <= 10:    

            self.__call__(reactor_list[12])
        

        elif position == 'Leo' or position == 'Leo' and degree >= 11 and degree <= 20:

            self.__call__(reactor_list[13])


        elif position == 'Leo' or position == 'Leo' and degree >= 21 and degree <= 30:

            self.__call__(reactor_list[14])


        elif position == 'Vir' or position == 'Virgo' and degree >= 0 and degree <= 10:

            self.__call__(reactor_list[15])


        elif position == 'Vir' or position == 'Virgo' and degree >= 11 and degree <= 20:

            self.__call__(reactor_list[16])


        elif position == 'Vir' or position == 'Virgo' and degree >= 21 and degree <= 30:

            self.__call__(reactor_list[17]) 


        elif position == 'Lib' or position == 'Libra' and degree >= 0 and degree <= 10:

            self.__call__(reactor_list[18])


        elif position == 'Lib' or position == 'Libra' and degree >= 11 and degree <= 20:

            self.__call__(reactor_list[19])


        elif position == 'Lib' or position == 'Libra' and degree >= 21 and degree <= 30:

            self.__call__(reactor_list[20])


        elif position == 'Sco' or position == 'Scorpio' and degree >= 0 and degree <= 10:

            self.__call__(reactor_list[21])


        elif position == 'Sco' or position == 'Scorpio' and degree >= 11 and degree <= 20:

            self.__call__(reactor_list[22])


        elif position == 'Sco' or position == 'Scorpio' and degree >= 21 and degree <= 30:

            self.__call__(reactor_list[23])


        elif position == 'Sag' or position == 'Sagittarius' and degree >= 0 and degree <= 10:

            self.__call__(reactor_list[24])


        elif position == 'Sag' or position == 'Sagittarius' and degree >= 11 and degree <= 20:

            self.__call__(reactor_list[25])


        elif position == 'Sag' or position == 'Sagittarius' and degree >= 21 and degree <= 30:

            self.__call__(reactor_list[26]) 


        elif position == 'Cap' or position == 'Capricorn' and degree >= 0 and degree <= 10:

            self.__call__(reactor_list[27])


        elif position == 'Cap' or position == 'Capricorn' and degree >= 11 and degree <= 20:    

            self.__call__(reactor_list[28])


        elif position == 'Cap' or position == 'Capricorn' and degree >= 21 and degree <= 30:

            self.__call__(reactor_list[29])


        elif position == 'Aqu' or position == 'Aquarius' and degree >= 0 and degree <= 10:

            self.__call__(reactor_list[30])


        elif position == 'Aqu' or position == 'Aquarius' and degree >= 11 and degree <= 20:

            self.__call__(reactor_list[31])

        

        elif position == 'Aqu' or position == 'Aquarius' and degree >= 21 and degree <= 30:

            self.__call__(reactor_list[32])

        
        elif position == 'Pis' or position == 'Pisces' and degree >= 0 and degree <= 10:

            self.__call__(reactor_list[33])


        elif position == 'Pis' or position == 'Pisces' and degree >= 11 and degree <= 20:

            self.__call__(reactor_list[34])


        elif position == 'Pis' or position == 'Pisces' and degree >= 21 and degree <= 30:

            self.__call__(reactor_list[35])
        

        else:


            raise ValueError('Invalid position')




class JungianActivationFunctions:


    def technique_mixer(self, orb_mappings):
        
        """
        Returns a tuple containing an identity string and a prompt string.
        The identity string is a creative writing prompt that asks the user to
        create a new spell based on the given orb mappings.
        The prompt string is a string that describes the orb mappings
        and asks the user to create a new spell based on them.

        Parameters
        ----------

        orb_mappings : str
            A string describing the orb mappings.

        Returns
        -------

        tuple
            A tuple containing the identity string and the prompt string.
        """
        identity = """"
            You are a fantasy creative writer.
         
        """
        prompt = f"""

            Come up with an action or spell based on the following techniques:

                {orb_mappings} 

        """

        return identity, prompt


    def monster_mixer(self, orb_mappings):
        

        """
        Returns a tuple containing an identity string and a prompt string.
        The identity string is a creative writing prompt that asks the user to
        create a new monster based on the given orb mappings.
        The prompt string is a string that describes the orb mappings
        and asks the user to create a new monster based on them.

        Parameters
        ----------

        orb_mappings : str
            A string describing the orb mappings.

        Returns
        -------

        tuple
            A tuple containing the identity string and the prompt string.
        """
        identity = """"
            You are a fantasy creative writer.
         
        """
        prompt = f"""

            Come up with a monster based on the following monsters:

                {orb_mappings} 

        """

        return identity, prompt




    def character_mixer(self, character_mappings):
    
        """
        Returns a tuple containing an identity string and a prompt string.
        The identity string is a creative writing prompt that asks the user to
        create a new character based on the given character mappings.
        The prompt string is a string that describes the character mappings
        and asks the user to create a new character based on them.

        Parameters
        ----------

        character_mappings : str
            A string describing the character mappings.

        Returns
        -------

        tuple
            A tuple containing the identity string and the prompt string.
        """
        identity = """"
            You are a fantasy creative writer.
         
        """
        prompt = f"""

            Come up with a new class chracter based on the following class carachters:

                {character_mappings} 

        """

        return identity, prompt

    def ego(self, samples):

        identity = """
            You are the head of a council. You review many opinions and take action based on the majority consensus prioritizing the creation of new things.

        """

        prompt = f"""

            Opinions:

                {samples}

        """

        return identity, prompt



    def superego(self, samples):

        identity = """
            You are the head of a council. You review many opinions and take action based on the majority consensus prioritizing self-preservation.

            You only trust the methods that were tried and succesful in the past. You prioritize survival at all costs - even if egotistical.

        """

        prompt = f"""

            Opinions:

                {samples}

        """

        return identity, prompt

    def shadow(self, samples):

        identity = """
            You are the head of a council. You review many opinions and take action based on the past.

            Your attention and action-taking is geared towards the uncomprehensible events of the past.  
            
            You project opinions of the past into current matters making incomplete knowledge the narrative you live by.

            You integrate and take decisions without understanding the consequences.

        """

        prompt = f"""

            Opinions:

                {samples}

        """

        return identity, prompt


    def spirit(self, samples):

        identity = """
            You are the head of a council. You review many opinions and take action based on the future.

            Your attention and action-taking is geared towards understading the ultimate meaning of things you are interested in.  

            You weight many opinions and always choose to take actions based on whats most interesting.
            

        """

        prompt = f"""

            Opinions:

                {samples}

        """

        return identity, prompt



    def one(self, ents):  
        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'explosion' with the following entities:
                
                {ents}

            """ 


        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'explosion' with the following entities:

                    {ents}

            """

            return self.identity, prompt

        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'explosion' with the following entities:

                    {ents}

            """

            return self.identity, prompt


        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'explosion' with the following entities:

                    {ents}

            """

            return self.identity, prompt


        
        else:

            raise ValueError('Invalid ammount of entities')


    def two(self, ents):

        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'lascerate' with the following entities:
                
                {ents}

            """ 

 
        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'lascerate' with the following entities:

                    {ents}

            """

            return self.identity, prompt

        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'lascerate' with the following entities:

                    {ents}

            """

            return self.identity, prompt


        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'lascerate' with the following entities:

                    {ents}

            """

            return self.identity, prompt


        
        else:

            raise ValueError('Invalid ammount of entities')


    def three(self, ents):

        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'slash' with the following entities:
                
                {ents}

            """ 

        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'slash' with the following entities:

                    {ents}

            """

            return self.identity, prompt

        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'slash' with the following entities:

                    {ents}

            """

            return self.identity, prompt


        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'slash' with the following entities:

                    {ents}

            """

            return self.identity, prompt
 
        else:

            raise ValueError('Invalid ammount of entities')




    def four(self, ents):
        
        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'bludgeoning' with the following entities:
                
                {ents}

            """ 

        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'bludgeoning' with the following entities:

                    {ents}

            """

            return self.identity, prompt

        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'bludgeoning' with the following entities:

                    {ents}

            """

            return self.identity, prompt


        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'bludgeoning' with the following entities:

                    {ents}

            """

            return self.identity, prompt

        
        else:

            raise ValueError('Invalid ammount of entities')


    def five(self, ents):

        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'trunk' with the following entities:
                
                {ents}

            """ 

        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'trunk' with the following entities:

                    {ents}

            """

            return self.identity, prompt

        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'trunk' with the following entities:

                    {ents}

            """

            return self.identity, prompt


        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'trunk' with the following entities:

                    {ents}

            """

            return self.identity, prompt


        
        else:

            raise ValueError('Invalid ammount of entities')





    def six(self, ents):
                
        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'rock' with the following entities:
                
                {ents}

            """ 

        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'rock' with the following entities:

                    {ents}

            """

            return self.identity, prompt

        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'rock' with the following entities:

                    {ents}

            """

            return self.identity, prompt


        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'rock' with the following entities:

                    {ents}

            """

            return self.identity, prompt


        
        else:

            raise ValueError('Invalid ammount of entities')





    def seven(self, ents):

        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'quartz' with the following entities:
                
                {ents}

            """ 


        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'quartz' with the following entities:

                    {ents}

            """

            return self.identity, prompt

        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'quartz' with the following entities:

                    {ents}

            """

            return self.identity, prompt


        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'quartz' with the following entities:

                    {ents}

            """

            return self.identity, prompt


        
        else:

            raise ValueError('Invalid ammount of entities')




    def eight(self, ents):
        
        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'echoes' with the following entities:
                
                {ents}

            """ 

        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'echoes' with the following entitiespell


                    {ents}

            """

            return self.identity, prompt

        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'echoes' with the following entities:

                    {ents}

            """

            return self.identity, prompt


        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'echoes' with the following entities:

                    {ents}

            """

            return self.identity, prompt


        
        else:

            raise ValueError('Invalid ammount of entities')



    def nine(self, ents):
        
        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'whispers' with the following entities:
                
                {ents}

            """ 

        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'whispers' with the following entities:

                    {ents}

            """

            return self.identity, prompt

        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'whispers' with the following entities:

                    {ents}

            """

            return self.identity, prompt


        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'whispers' with the following entities:

                    {ents}

            """

            return self.identity, prompt


        
        else:

            raise ValueError('Invalid ammount of entities')





    def tenth(self, ents):
            
        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'rain' with the following entities:
                
                {ents}

            """ 


        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or sklil combining the concept 'rain' with the following entities:

                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'rain' with the following entities:

                    {ents}

            """



        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'rain' with the following entities:

                    {ents}

            """

 
        else:

            raise ValueError('Invalid ammount of entities')


        return self.identity, prompt




    def eleven(self, ents):
                
        

        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'river' with the following entities:
                
                {ents}

            """ 

        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'river' with the following entities:

                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'river' with the following entities:

                    {ents}

            """



        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'river' with the following entities:

                    {ents}

            """

        
        else:

            raise ValueError('Invalid ammount of entities')
        
        return self.identity, prompt





    def twelve(self, ents):
                 
        identity = """

            You are a creative fantasy writer who comes up with spells, monsters and chracters based on specified entities.

        """

        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'roots' with the following entities:
                
                {ents}

            """ 


        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'roots' with the following entities:

                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'roots' with the following entities:

                    {ents}

            """



        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""
 
                Come up with a class character combining the concept 'roots' with the following entities:

                    {ents}

            """



        
        else:

            raise ValueError('Invalid ammount of entities')

        return self.identity, prompt



    
    def thirteen(self, ents):
        
        identity = """

            You are a creative fantasy writer who comes up with spells, monsters and chracters based on specified entities.

        """

        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'wood' with the following entities:
                
                {ents}

            """ 

        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'wood' with the following entities:

                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'wood' with the following entities:

                    {ents}

            """



        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'wood' with the following entities:

                    {ents}

            """
        
        else:

            raise ValueError('Invalid ammount of entities')

        return self.identity, prompt



    def fourteen(self, ents):

        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'blood' with the following entities:
                
                {ents}

            """ 


        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'blood' with the following entities:

                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'blood' with the following entities:

                    {ents}

            """



        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'blood' with the following entities:

                    {ents}

            """
 
        else:

            raise ValueError('Invalid ammount of entities')


        return self.identity, prompt



    def fifteen(self, ents):
        
        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'thunder' with the following entities:
                
                {ents}

            """ 


        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'thunder' with the following entities:

                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'thunder' with the following entities:

                    {ents}

            """



        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'thunder' with the following entities:

                    {ents}

            """

        
        else:

            raise ValueError('Invalid ammount of entities')


        return self.identity, prompt


    def sixteen(self, ents):
        

        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'charring' with the following entities:
                
                {ents}

            """ 


        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'charring' with the following entities:

                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'charring' with the following entities:

                    {ents}

            """



        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'charring' with the following entities:

                    {ents}

            """
        
        else:

            raise ValueError('Invalid ammount of entities')

        return self.identity, prompt



    def seventeen(self, ents):
        
        
        identity = """
            You are a creative fantasy writer who comes up with spells, monsters and chracters based on specified entities.

        """
        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'filtration' with the following entities:
                
                {ents}

            """ 

        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'filtration' with the following entities:

                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'filtration' with the following entities:

                    {ents}

            """



        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'filtration' with the following entities:

                    {ents}

            """
        
        else:

            raise ValueError('Invalid ammount of entities')

        return self.identity, prompt



    def eighteen(self, ents):
                
        
        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'crystallization' with the following entities:
                
                {ents}

            """ 

        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'crystallization' with the following entities:

                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'crystallization' with the following entities:

                    {ents}

            """



        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'crystallization' with the following entities:

                    {ents}

            """
        
        else:

            raise ValueError('Invalid ammount of entities')

        return self.identity, prompt




    def nineteen(self, ents):
           
        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'rhythm' with the following entities:
                
                {ents}

            """ 


        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'rhythm' with the following entities:

                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'rhythm' with the following entities:

                    {ents}

            """



        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'rhythm' with the following entities:

                    {ents}

            """

        
        else:

            raise ValueError('Invalid ammount of entities')


        return self.identity, prompt



    def twenty(self, ents):

        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'meteor' with the following entities:
                
                {ents}

            """ 

        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'wind' with the following entities:

                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'wind' with the following entities:

                    {ents}

            """



        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'wind' with the following entities:

                    {ents}

            """
        
        else:

            raise ValueError('Invalid ammount of entities')

        return self.identity, prompt



    def twentyone(self, ents):
        
        if len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'hailstorm' with the following entities:


                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'hailstorm' with the following entities:

                    {ents}

            """



        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'hailstorm' with the following entities:

                    {ents}

            """

        
        else:

            raise ValueError('Invalid ammount of entities')


        return self.identity, prompt




    def twentytwo(self, ents):
              

        if len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'ice' with the following entities:

                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'ice' with the following entities:

                    {ents}

            """



        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'ice' with the following entities:

                    {ents}

            """

        
        else:

            raise ValueError('Invalid ammount of entities')

        return self.identity, prompt


    def twentythree(self, ents):    
        
              
        if len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'phoenix' with the following entities:

                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'phoenix' with the following entities:

                    {ents}

            """



        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'phoenix' with the following entities:

                    {ents}

            """

        
        else:

            raise ValueError('Invalid ammount of entities')


        return self.identity, prompt



    def twentyfour(self, ents):
                
        if len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'venom' with the following entities:

                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'venom' with the following entities:

                    {ents}

            """



        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'venom' with the following entities:

                    {ents}

            """

        
        else:

            raise ValueError('Invalid ammount of entities')

        return self.identity, prompt



    def twentyfive(self, ents):
                  
        if len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'piercing' with the following entities:

                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'piercing' with the following entities:

                    {ents}

            """



        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'piercing' with the following entities:

                    {ents}

            """

        
        else:

            raise ValueError('Invalid ammount of entities')

        return self.identity, prompt


    def twentysix(self, ents):

        self.identity = """
            You are a creative fantasy writer who comes up with spells, monsters and chracters based on specified entities.

        """


        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'meteor' with the following entities:
                
                {ents}

            """ 

        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'firestorm' with the following entities:

                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'firestorm' with the following entities:

                    {ents}

            """



        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'firestorm' with the following entities:

                    {ents}

            """
        
        else:

            raise ValueError('Invalid ammount of entities')


        return self.identity, prompt




    def twentyseven(self, ents):

        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'meteor' with the following entities:
                
                {ents}

            """ 

        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'meteor' with the following entities:

                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'meteor' with the following entities:

                    {ents}

            """



        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'meteor' with the following entities:

                    {ents}

            """
        
        else:

            raise ValueError('Invalid ammount of entities')

        return self.identity, prompt




    def twentyeight(self, ents):
        
        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'tremor and earthquake' with the following entities:
                
                {ents}

            """ 

        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'tremor or earthquake' with the following entities:

                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'tremor or earthquake' with the following entities:

                    {ents}

            """



        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'tremor or earthquake' with the following entities:

                    {ents}

            """
        
        else:

            raise ValueError('Invalid ammount of entities')

        return self.identity, prompt




    def twentynine(self, ents):

        identity = """
            You are a creative fantasy writer who comes up with spells, monsters and chracters based on specified entities.

        """
        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'gravity' with the following entities:
                
                {ents}

            """ 

        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'gravity' with the following entities:

                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'gravity' with the following entities:

                    {ents}

            """



        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'gravity' with the following entities:

                    {ents}

            """

        
        else:

            raise ValueError('Invalid ammount of entities')

        return self.identity, prompt


    def thirty(self, ents):

        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'darkness' with the following entities:
                
                {ents}

            """ 


        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'darkness' with the following entities:

                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'darkness' with the following entities:

                    {ents}

            """



        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'darkness' with the following entities:

                    {ents}

            """

        
        else:

            raise ValueError('Invalid ammount of entities')


        return self.identity, prompt



    def thirtyone(self, ents):
        
        identity = """
            You are a creative fantasy writer who comes up with spells, monsters and chracters based on specified entities.

        """

        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'static and charge' with the following entities:
                
                {ents}

            """ 

        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'static or charge' with the following entities:

                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'static or charge' with the following entities:

                    {ents}

            """



        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'static or charge' with the following entities:

                    {ents}

            """

        
        else:

            raise ValueError('Invalid ammount of entities')

        return self.identity, prompt




    def thirtytwo(self, ents):    
            
        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'greatsword' with the following entities:
                
                {ents}

            """ 

        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'greatsword' with the following entities:

                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'greatsword' with the following entities:

                    {ents}

            """

        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'greatsword' with the following entities:

                    {ents}

            """

        
        else:

            raise ValueError('Invalid ammount of entities')
        
        return self.identity, prompt




    def thirtythree(self, ents):
                
        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept object and 'shadows' with the following entities:
                
                {ents}

            """ 


        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'shadows' with the following entities:

                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'shadows' with the following entities:

                    {ents}

            """



        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'shadows' with the following entities:

                    {ents}

            """



        
        else:

            raise ValueError('Invalid ammount of entities')


        return self.identity, prompt



    def thirtyfour(self, ents):


        if len(ents) == 1:

            prompt = f"""

                Come up with a fantasy object combining the concept 'ghostly' with the following entities:
                
                {ents}

            """ 

        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'ghostly' with the following entities:

                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'ghastly' with the following entities:

                    {ents}

            """


        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'ghastly' with the following entities:

                    {ents}

            """

        
        else:

            raise ValueError('Invalid ammount of entities')

        return self.identity, prompt


    def thirtyfive(self, ents):

        if len(ents) == 1:
 
            prompt = f"""

                Come up with a fantasy object combining the concept 'vacuum' with the following entities:

                    {ents}

            """        

        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'vacuum' with the following entities:

                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'vacuum' with the following entities:

                    {ents}

            """

        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'vacuum' with the following entities:

                    {ents}

            """

        
        else:

            raise ValueError('Invalid ammount of entities')

        return self.identity, prompt



    def thirtysix(self, ents):

        identity = """
            You are a creative fantasy writer who comes up with spells, monsters and chracters based on specified entities.

        """

        if len(ents) == 1:

            prompt = f"""
                Come up with a fantasy object based on the concept of lighting with the following entities:

                    {ents}

            """


        elif len(ents) >= 2 or len(ents) < 4:
             

            prompt = f"""

                Come up with a spell or skill combining the concept 'lighting' with the following entities:

                    {ents}

            """


        elif len(ents) > 5 and len(ents) < 8:

            prompt = f"""

                Come up with a monster combining the concept 'lighting' with the following entities:

                    {ents}

            """


        elif len(ents) > 9 and len(ents) < 12:

            prompt = f"""

                Come up with a class character combining the concept 'lighting' with the following entities:

                    {ents}

            """

        
        else:

            raise ValueError('Invalid ammount of entities')


        return self.identity, prompt


class JungianObjectReducer:


    def __init__(self) -> None:
        pass


    def one(self, ents):

        identity = """
            You are a creative fantasy writer who comes up with fantasy objects based on specified entities.

        """

        prompt = f"""

            Come up with a fantasy helmet or occular effects based on the following entities:
            

            {ents}

        """
        
        return identity, prompt



    def two(self, ents):

        identity = """
            You are a creative fantasy writer who comes up with fantasy objects based on specified entities.

        """

        prompt = f"""

            Come up with a fantasy shield based on the following entities:

            {ents}

        """
        
        return identity, prompt
    
    def three(self, ents):

        identity = """
            You are a creative fantasy writer who comes up with fantasy objects based on specified entities.

        """

        prompt = f"""

            Come up with a fantasy horn based on the following entities:

            {ents}

        """
        
        return identity, prompt
        

    def four(self, ents):

        identity = """
            You are a creative fantasy writer who comes up with fantasy objects based on specified entities.

        """

        prompt = f"""

            Come up with a fantasy amulet based on the following entities:

            {ents}

        """
        
        return identity, prompt

    def five(self, ents):

        identity = """
            You are a creative fantasy writer who comes up with fantasy objects based on specified entities.

        """

        prompt = f"""

            Come up with a fantasy hair accesory based on the following entities:

            {ents}

        """
        
        return identity, prompt

    def six(self, ents):

        identity = """
            You are a creative fantasy writer who comes up with fantasy objects based on specified entities.

        """

        prompt = f"""

            Come up with a fantasy ring based on the following entities:

            {ents}

        """
        
        return identity, prompt


    def seven(self, ents):

        identity = """
            You are a creative fantasy writer who comes up with fantasy objects based on specified entities.

        """

        prompt = f"""

            Come up with a fantasy diadem or instrument based on the following entities:

            {ents}

        """
        
        return identity, prompt 
    

    def eight(self, ents):

        identity = """
            You are a creative fantasy writer who comes up with fantasy objects based on specified entities.

        """

        prompt = f"""

            Come up with a fantasy sword based on the following entities:

            {ents}

        """
        
        return identity, prompt


    def eight(self, ents):

        identity = """
            You are a creative fantasy writer who comes up with fantasy objects based on specified entities.

        """

        prompt = f"""

            Come up with a fantasy sword based on the following entities:

            {ents}

        """
        
        return identity, prompt

    def nine(self, ents):

        identity = """
            You are a creative fantasy writer who comes up with fantasy objects based on specified entities.

        """

        prompt = f"""

            Come up with a fantasy set of thigs or pants based on the following entities:

            {ents}

        """
        
        return identity, prompt


    def ten(self, ents):

        identity = """
            You are a creative fantasy writer who comes up with fantasy objects based on specified entities.

        """

        prompt = f"""

            Come up with a fantasy clock or boots based on the following entities:

            {ents}

        """
        
        return identity, prompt


    def eleven(self, ents):

        identity = """
            You are a creative fantasy writer who comes up with fantasy objects based on specified entities.

        """

        prompt = f"""

            Come up with a fantasy breastplate based on the following entities:

            {ents}

        """
        
        return identity, prompt


    def twelve(self, ents):

        identity = """
            You are a creative fantasy writer who comes up with fantasy objects based on specified entities.

        """

        prompt = f"""

            Come up with a fantasy mask based on the following entities:

            {ents}

        """
        
        return identity, prompt


