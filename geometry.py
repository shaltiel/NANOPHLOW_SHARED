import local_utils as util


class Geometry:
    """All geometeries subclasses should call generate and end up in a template folder"""
    def __init__(self, name, path):
        self.name = name;
        self.path = path;
        self.data_file = "path to executed geometry"
        self.template_folder = path + "/Template"
        self.is_generated = False

    def generate(self):
        raise NotImplemented("implement a generate method in child")


class BenchmarkGeometry(Geometry):
    """This is the only geometry for now of polymer of n monomers, also be used as the demo"""

    def __init__(self,name):
        path = util.paths.PROJECT + "/BenchmarkGeometry"
        Geometry.__init__(self, name, path);

    def generate(self, lx=20, ly=20, lz=20, n_monomers=30, sol_frac=0.1):
        self.modify_script(lx, ly, lz, n_monomers, sol_frac);
        import subprocess
        print "start"
        subprocess.call("")
        print "end"
        self.is_generated = True

    def modify_script(self, lx, ly, lz, n_monomers, sol_frac):
        # change paths
        program_path=self.path+"/programs/poly"
        file_path = self.path + "/initial_geometry/generate_data.sh";
        util.replace(file_path=file_path,
                     origin_line=r"CMD_SLAB='/frenkelscratch/sr802/DiffusioP/programs/poly'",
                     new_line="CMD_SLAB='" + program_path + "'")
        # change parameters
        util.replace(file_path, "LX=20","LX="+str(lx))
        util.replace(file_path, "LY=20", "LY=" + str(ly))
        util.replace(file_path, "LZ=20", "LZ=" + str(lz))
        util.replace(file_path, "PN=30", "PN=" + str(n_monomers))
        util.replace(file_path, "SOLF=0.1", "SOLF=" + str(sol_frac))

