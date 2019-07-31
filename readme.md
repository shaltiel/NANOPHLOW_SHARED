### Latest Changes 24/7/19

Hi, 
I added the geometry configuration class which should generate the geometry according to your instruction. I didnt want to try to compile the fortran cod. but the infrastracture of replacing and puting parameters are in the class geometry. There is the first subclass BenchmarkGeometry which does that, I guess the end goal is that the geometry class can have many ways to create geometries but all what matters is that it will have a template target, so the study object can get it.

I added the equlibrium subclass under the study class so it is easy to call it just as under subclass of study.
So you can see the scheme example i wrote on the main in restart launcher. 
Let me know what you think.
Best,
Shaltiel 



### Changes to qsub folder of Simon
Hi Simon, 

I did some changes to the code scheme so it would be more modular and maybe relevant for this NANOPHLOW software.

I attach the qsub directory with the changes, I didnt want to put it in your repo at the moment. I followed your starting point of simulation class and just decorated the rest of the code with few other classes:

InputModifier class and its subclasses: 

instead of applying the replacements of lammps input in the main, the sim gets a dictionary of all parameters, and there is a method belongs to the simulation class object, that will go through all the parameters and replace in the input.

        for field in param_dic:
            InputModifier.call_modifier(field, self)
           
Every parameter has a sub class which contains the instruction of the replacement in the input file. 

Study class (StudyManager file)
contains the simulations objects and manage them. If I understand right, running the start configurations is one specific scheme so there is example class of RestartStudy derived form study. 
I guess an idea can be that beside restart study class will be also equilibrium study and so on. So the user can control and create the project from above without interacting directly with the simulation object.


With the changes above, the example which does the same as previous but with thus changes is found in 'launch_restart.py' file.


There is also local_util class file to handle abs paths and directories which i decided to work with so i can understand easily how it works.

So you can take a look at it and tell me what you think. Then if you think its relevant, we can continue forward and add the equalibrium, and analysis parts which I don't know where they are taken from.
Shaltiel  
