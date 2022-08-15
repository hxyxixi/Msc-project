# Msc-project
Hi,I am very glad that you can see my Project ! Here I will give a general description of how my project works!

1: The diagram below shows the structure of the project's engineering documentation.

![Framework](https://user-images.githubusercontent.com/97906259/184588335-d1f07360-071b-4bb1-8b7b-86e9bd1f7511.PNG)

2: P.S.:If you want to run this project file successfully, please follow the system error instructions to download and install the required tools.

3: The choice of whether to train or test the model is changed in the common folder under arguments.py.
  Tain Mode: Load_Mode:'Flase' and Learn:'True'
  Test Mode: Load_Mode:'True' and Learn:'Flase'
  
4: get_map.py is environment file:
  Our main elements in this document include: drawing the game environment, describing the rules of the game and inserting noise into the environment.
  
5: About Inserting noise into the environment:

![noise](https://user-images.githubusercontent.com/97906259/184597679-fd15c5fb-03fe-43f4-9664-4ffbd64fd6f7.PNG)

   We use the codes in the diagram above to do this. 
   If adding noise use the first and second lines of codes. 
   If no noise is added use the last two lines of codes.
   
6：The images in the results folder are generated via runner.py. We use it to keep the success rate and the reward values obtained in each training round.

7.main.py: The main file of the program. To start training or testing, please run main.py directly.
