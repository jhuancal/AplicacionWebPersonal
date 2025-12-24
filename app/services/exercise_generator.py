import random

class ExerciseGeneratorService:
    @staticmethod
    def generate(operation):
        """
        Generates an exercise based on the Edu_OperacionMatematica entity.
        Returns a dict: { 'question': str, 'answer': str, 'options': list }
        """
        func_name = operation.FuncionSistema
        
        if func_name == 'gen_poly_sum':
            return ExerciseGeneratorService._gen_poly_sum()
        elif func_name == 'gen_linear_eq':
            return ExerciseGeneratorService._gen_linear_eq()
        else:
            return {
                'question': f"Error: Unknown generator {func_name}",
                'answer': "0",
                'options': ["0", "1", "2", "3"]
            }

    @staticmethod
    def _gen_poly_sum():
        # (ax + b) + (cx + d)
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        c = random.randint(1, 9)
        d = random.randint(1, 9)
        
        question = f"({a}x + {b}) + ({c}x + {d})"
        
        answ_coeff = a + c
        answ_const = b + d
        correct_answer = f"{answ_coeff}x + {answ_const}"
        
        # Generate distractors
        options = set()
        options.add(correct_answer)
        
        while len(options) < 4:
            fake_a = answ_coeff + random.randint(-3, 3)
            fake_b = answ_const + random.randint(-3, 3)
            if fake_a == 0: fake_a = 1
            options.add(f"{fake_a}x + {fake_b}")
            
        return {
            'question': f"Simplify: {question}",
            'answer': correct_answer,
            'options': list(options)
        }

    @staticmethod
    def _gen_linear_eq():
        # ax + b = c  ->  ax = c - b  -> x = (c - b) / a
        # make sure x is integer
        x = random.randint(1, 10)
        a = random.randint(2, 5)
        b = random.randint(1, 20)
        c = (a * x) + b
        
        question = f"Solve for x: {a}x + {b} = {c}"
        correct_answer = str(x)
        
        options = set()
        options.add(correct_answer)
        
        while len(options) < 4:
            fake_x = x + random.randint(-5, 5)
            if fake_x != x:
                options.add(str(fake_x))
        
        return {
            'question': question,
            'answer': correct_answer,
            'options': list(options)
        }
