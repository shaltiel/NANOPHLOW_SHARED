
import shutil
from simulation_utilities import simulation
from local_utils import paths
import Lammps.core_functions as cf
'''Create and manage simulations of certain type'''


class Study:
    def __init__(self, name):
        self.sims = [];
        self.name = name;

    def prepare_simulations(self):
        for sim in self.sims:
            sim.create_folder()
            sim.create_qsub('short', 1, 16, 24, 'input.lmp')  # default?
            sim.modify_fields_input()
            sim.flag_prepared_to_run = True

    def run_simulations(self):
        for sim in self.sims:
            sim.run_simulation();

#   ----------------------------------------------------------------------


class Equilibration(Study):
    def __init__(self, name, root_sim, geometry, wall_time=24, suffix_id_param="Equalibrium"):
        Study.__init__(self, name)
        self.sim_folder = root_sim + '/' + name + '_%s' % suffix_id_param
        self.geometry = geometry
        self.template = geometry.template_folder
        self.wall_time = wall_time

    def prepare_simulations(self):
        for sim in self.sims:
            sim.create_folder()
            sim.create_qsub('short', 1, 16, self.wall_time, 'input.lmp')  # default?
            sim.modify_fields_input()
            sim.flag_prepared_to_run = True

    def add_simulation(self, params_dic):
        shutil.rmtree(self.sim_folder, ignore_errors=True)
        sim = simulation(self.sim_folder, self.template, self.name, params_dic)
        self.sims.append(sim)


class RestartStudy(Study):
    def __init__(self, name, root_sim, template, n_conf, suffix_id_param):
        Study.__init__(self, name)
        self.restart_files = paths.get_restart_files();
        self.sim_folder = root_sim + '/' + name + '_%s' % suffix_id_param

        times = cf.extract_digits(self.restart_files)
        times = [str(int(time[-1])) for time in times]
        # Takign the last N configurations
        conf_times = times[-n_conf:]
        self.files_analysis = cf.parameter_finder(self.restart_files, conf_times)
        self.template = template

    def add_all_simulations(self, params_dic):
        for i in self.files_analysis:
            self.add_simulation(self.restart_files[i], params_dic)

    def add_simulation(self, restart_file, params_dic):
        shutil.rmtree(self.sim_folder, ignore_errors=True)
        time = int(cf.extract_digits(restart_file)[-1])
        name = str(time)
        sim = simulation(self.sim_folder, self.template, name, restart_file, params_dic)
        self.sims.append(sim)
