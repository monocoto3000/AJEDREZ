import xml.etree.ElementTree as ET
import re

class TuringMachine:
    def __init__(self, xml_file):
        self.states = {} 
        self.transitions = []
        self.initial_state = None
        self.final_states = set()
        self.load_turing_machine(xml_file)
        
    def load_turing_machine(self, xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for state in root.find('automaton').findall('state'):
            state_id = state.get('id')
            state_name = state.get('name')
            is_initial = state.get('initial') == "true"
            is_final = state.get('final') == "true"
            
            self.states[state_id] = state_name
            if is_initial:
                self.initial_state = state_id
                print(f"Initial state set to: {self.initial_state}")
            if is_final:
                self.final_states.add(state_id)

        if self.initial_state is None:
            print("Warning: No initial state found.")

        for transition in root.find('automaton').findall('transition'):
            from_state = transition.find('from').text
            to_state = transition.find('to').text
            read_value = transition.find('read').text if transition.find('read') is not None else None
            write_value = transition.find('write').text if transition.find('write') is not None else None
            move_direction = transition.find('move').text if transition.find('move') is not None else 'S'
            self.transitions.append((from_state, to_state, read_value, write_value, move_direction))
    
    def is_valid_transition(self, current_state, char):
        """
        Returns the next state, write value, and move direction if there is a valid transition, otherwise None.
        """
        for (from_state, to_state, read_value, write_value, move_direction) in self.transitions:
            # Allow transition if read_value is None (meaning it should match any character or space)
            if from_state == current_state:
                if read_value is None or self.match_transition(read_value, char):
                    return to_state, write_value, move_direction
        return None, None, None

    def match_transition(self, read_value, char):
        """
        Matches the input character with the transition's read value.
        """
        return read_value == char

    def evaluate_string(self, input_string):
        """
        Evaluates a string character by character using the Turing machine's transitions.
        Returns the final tape content if the machine reaches a final state.
        """
        if not self.initial_state:
            print("Error: No initial state configured.")
            return None

        # Add underscores to the input string for Turing machine blank representation
        input_string = f"_{input_string}_"

        print(self.final_states)
        
        tape = list(input_string)  # Convert input string to list for mutability
        head_position = 1  # Start at the first significant character, skipping the initial underscore
        current_state = self.initial_state

        while True:
            # Check if the Turing Machine reached a final state and stop if so
            if current_state in self.final_states:
                print("Reached a final state during processing.")
                final_content = ''.join(tape).strip('_')  # Remove leading and trailing underscores
                print("Final tape content:", final_content)
                return final_content

            # Get the current character under the head or default to '_'
            current_char = tape[head_position] if head_position < len(tape) else '_'
            next_state, write_value, move_direction = self.is_valid_transition(current_state, current_char)

            # If no valid transition is found, halt the machine
            if next_state is None:
                print(f"No valid transition from state {current_state} on '{current_char}'. Halting.")
                return None

            # Write to the tape if there's a specified write_value
            if head_position < len(tape):
                tape[head_position] = write_value if write_value is not None else current_char
            else:
                tape.append(write_value if write_value is not None else '_')

            # Move the head based on direction
            if move_direction == 'R':
                head_position += 1
            elif move_direction == 'L':
                head_position = max(0, head_position - 1)

            # Update current state to the next state
            current_state = next_state

            print(f"Current State: {current_state}, Head Pos: {head_position}, Tape: {''.join(tape)}")


# Ejemplo de uso
if __name__ == "__main__":
    turing_machine = TuringMachine("MT1.xml")
    test_string = input("Ingrese el string: ")
    result = turing_machine.evaluate_string(test_string)
    if result is not None:
        print("Resultado final en la cinta:", result)
    else:
        print("La máquina no aceptó la cadena.")