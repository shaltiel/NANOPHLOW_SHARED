import Lammps.core_functions as cf
'''A modifier of the input according to the field parameter name. 
Each field is a child class of input modifier
and will have its own string replacement instruction'''


class InputModifier:
    def __init__(self, sim, file_name):
        self.sim = sim
        self.file_path = sim.folder + '/' + file_name
        self.flag_modified = False

    def modify_file(self, field, str):
        try:
            cf.modify_file(self.file_path, field, str)
            return True
        except StandardError:
            print("problem with modifying")

    @classmethod
    def call_modifier(cls, field, sim):
        return eval(field)(sim)
# ------------------------------------------------------------------------


class Force(InputModifier):
    def __init__(self, sim):
        file_name = "input.lmp"
        InputModifier.__init__(self, sim, file_name)
        self.str = 'variable\tforce equal %s\n' % sim.params_dic["Force"]
        self.flag_modified = self.modify_file('force', self.str);


class Epsilon(InputModifier):
    def __init__(self, sim):
        file_name = "in.interaction"
        InputModifier.__init__(self, sim, file_name)
        self.str = 'pair_coeff\t2 3 %s 1.0\n'%sim.params_dic["Epsilon"]
        self.flag_modified = self.modify_file('2 3', self.str);


class Restart(InputModifier):
    def __init__(self, sim):
        file_name="input.lmp"
        InputModifier.__init__(self, sim, file_name)
        value_modify = sim.initial_conf.split('/')[-1]
        self.str = 'read_restart\t%s\n'%value_modify
        self.flag_modified = self.modify_file('read_restart', self.str);


class Nconf(InputModifier):
    def __init__(self, sim):
        file_name="input.lmp"
        InputModifier.__init__(self, sim, file_name)
        print("nothing to modify for Nconf")
