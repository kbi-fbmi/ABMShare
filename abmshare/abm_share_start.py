import abmshare.extension_controller as exct
import argparse
import os

if __name__=="__main__":
    parser =  argparse.ArgumentParser(description='Short sample app')
    parser.add_argument('-c','--config')
    parser.add_argument('-v','--validation', nargs='?', default=False, const=True, choices=[True, False, 'true', 'True', 'false', "False"])
    parser.add_argument('-g', '--grid_compute', nargs='?', default=False, const=True, choices=[True, False, 'true', 'True', 'false', "False"])
    parser.add_argument('-u','--user')
    parser.add_argument('-t','--test')
    args=parser.parse_args() 
    
    if args.grid_compute in ['true', 'True', True]:
        grid_compute = True
    else:
        grid_compute = False
    
    if args.validation in ['true', 'True', True]:
        args.validate = True
    else:
        args.validate = False

    if args.test in ['true', 'True', True]:
        args.test = True
    else:
        args.test = False

    user=args.user or os.getlogin()


    meh = exct.ExtensionController(configuration=args.config,grid_compute=grid_compute,grid_user=user,validate=args.validate,test=args.test) #args.config
    print("Everything is done")