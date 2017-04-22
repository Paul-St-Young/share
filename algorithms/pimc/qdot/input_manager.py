class InputManager:
    def __init__(self):
        self.inp = dict()
    # end def

    def parse_command_line(self):
	import argparse
	parser = argparse.ArgumentParser()

        # define SHO
	parser.add_argument('-l','--lam',type=float
            ,default=0.5,help='1/(2*mass)')
	parser.add_argument('-o','--omega',type=float
            ,default=10.0,help='spring freq.')

        # define system
	parser.add_argument('-nptcl','--nptcl',type=int
            ,default=1,help='number of particles')
	parser.add_argument('-ndim','--ndim',type=int
            ,default=1,help='number of spatial dimension')

        # specify temperature
	parser.add_argument('-b','--beta',type=float
            ,default=1.0,help='inverse temp.')

        # path integral inputs
        parser.add_argument('-ns','--nslice',type=int
            ,default=2,help='number of time slices')

        # Monte Carlo inputs
	parser.add_argument('-n','--nsample',type=int
            ,default=100,help='number of samples to collect')
	parser.add_argument('-bs','--block_size',type=int
            ,default=5,help='steps per block to remove autocorrelation')
	parser.add_argument('-s','--sig',type=float
            ,default=0.5,help='step size')
	parser.add_argument('-neq','--nequil',type=int
            ,default=5,help='number of equilibration steps')


	args = parser.parse_args()
        """ # use vars() instead
        cmd_inp = {
            'lam':args.lam,
            'omega':args.omega,
            'beta':args.beta,
            'nptcl':args.num_particle,
            'ndim':args.num_dimension,
            'nslice':args.nslice,
            'nsample':args.nsample,
            'block_size':args.block_size,
            'sig':args.sig,
            'nequil':args.nequil,
        }
        """

        return args
    # end def parse_command_line

    def parse_input_file(self,fname):
        with open(fname,'r') as fp:
            text = fp.read()
        # end with
        # get all key-value pairs separated by '='
        key_val = dict([line.split('=') for line in text.split('\n') if '=' in line])
        # interpret value types
    # end def


# end class

if __name__ == '__main__':

    inp_manager = InputManager()
    args = inp_manager.parse_command_line()
    print vars(args).keys()

    #print inp_manager.parse_input_file('sho.txt')

