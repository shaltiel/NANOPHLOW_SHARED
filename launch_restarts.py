#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 09:24:03 2019
"Creates replicas of simulations starting from configurations during the equilibration"
@author: sr802
"""

import Lammps.core_functions as cf
import argparse
from local_utils import paths
import StudyManager as Study


# ------------- SE: possible way to interface ------------------
import Lammps.core_functions as cf
import argparse
from local_utils import paths
import StudyManager as Study
import geometry as geometry


# ------------- SE: possible way to interface ------------------
def main(name, root_sim, template, run_ready, params_dic):

    # -------------- Creating the geometry ---------------------

    default_geo = geometry.BenchmarkGeometry("polymer geometry")
    default_geo.generate(n_monomers=30, sol_frac=0.1)

    # ----------- Equilibrium run on geometry ------------------

    # setting up equilibration study from geometry
    study_eq = Study.Equilibration(name="polymer30_eq",
                                        root_sim=root_sim,
                                        geometry=default_geo,
                                        wall_time=48)
    study_eq.add_simulation(params_dic)
    study_eq.prepare_simulations()
    study_eq.run_simulations()

    # - Run simulation to calc. force from n configurations  -
    # in the tool should be indicate when eq is finished.

    # example of force study
    params_dic["Force"] = args.force

    # setting up simulation study from input configurations
    study_example = Study.RestartStudy(name=name,
                                       root_sim=root_sim,
                                       template=template,
                                       n_conf=params_dic["Nconf"],
                                       suffix_id_param=params_dic["Force"])

    study_example.add_all_simulations(params_dic)
    study_example.prepare_simulations()
    # running all simulations and saving outputs
    if run_ready: study_example.run_simulations()
# --------------------------------------------------------------


if __name__ == "__main__":
    """
    THIS IS VERY SPECIFIC
    The arguments of this depend on the application
    """
    parser = argparse.ArgumentParser(description='Launch simulations from restart',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-name', metavar='name',help='Name of the folder to keep all the simulations',default='mu_force')
    parser.add_argument('-conf_folder', metavar='path_restart',help='Directory of the restart files',default=paths.restart_files)
    parser.add_argument('-template', metavar='path_template',help='Directory to take as template',default= paths.template)
    parser.add_argument('-root_sim', metavar='root directory',help='Directory to create the folder for the simulations',default=paths.sim_outputs)
    parser.add_argument('-n_conf',metavar='n conf',help='number of configurations starting from the last',default=5,type=int)
    parser.add_argument('-epsilon',metavar='epsilon',help='monomer solute interaction',default=3.0,type=float)
    parser.add_argument('-force',metavar='force',help='Force on the solutes',default=0.01,type=float)
    parser.add_argument('-run',metavar='run',help='Define if run simulations or not. If not, just creates the folder structure',default=False,type=cf.str2bool)

    args = parser.parse_args()

    params_dic_input = {"Epsilon": args.epsilon,
                 "Force": args.force,
                 "Nconf": args.n_conf,
                 "Restart": -1}

    main(args.name, args.root_sim, args.template, args.run, params_dic_input)

