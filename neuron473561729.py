'''
Defines a class, Neuron473561729, of neurons from Allen Brain Institute's model 473561729

A demo is available by running:

    python -i mosinit.py
'''
class Neuron473561729:
    def __init__(self, name="Neuron473561729", x=0, y=0, z=0):
        '''Instantiate Neuron473561729.
        
        Parameters:
            x, y, z -- position offset
            
        Note: if name is not specified, Neuron473561729_instance is used instead
        '''
        
        self._name = name        
        # load the morphology
        from load_swc import load_swc
        load_swc('Gad2-IRES-Cre_Ai14_IVSCC_-172679.03.01.01_471076778_m.swc', self,
                 use_axon=False, xshift=x, yshift=y, zshift=z)

        # custom axon (works because dropping axon during import)
        from neuron import h
        self.axon = [h.Section(cell=self, name='axon[0]'),
                     h.Section(cell=self, name='axon[1]')]
        for sec in self.axon:
            sec.L = 30
            sec.diam = 1
            sec.nseg = 1
        self.axon[0].connect(self.soma[0](0.5))
        self.axon[1].connect(self.axon[0](1))
        self.all += self.axon
        
        self._insert_mechanisms()
        self._discretize_model()
        self._set_mechanism_parameters()
    
    def __str__(self):
        if self._name is not None:
            return self._name
        else:
            return "Neuron473561729_instance"
                
    def _insert_mechanisms(self):
        from neuron import h
        for sec in self.all:
            sec.insert("pas")
        for mech in [u'CaDynamics', u'Ca_HVA', u'Ca_LVA', u'Ih', u'Im_v2', u'K_T', u'Kd', u'Kv2like', u'Kv3_1', u'NaV', u'SK']:
            self.soma[0].insert(mech)
    
    def _set_mechanism_parameters(self):
        from neuron import h
        for sec in self.all:
            sec.Ra = 42.45
            sec.e_pas = -90.7373962402
        
        for sec in self.axon:
            sec.cm = 2.06
            sec.g_pas = 0.000382856697846
        for sec in self.dend:
            sec.cm = 2.06
            sec.g_pas = 1.15951469298e-05
        for sec in self.soma:
            sec.cm = 2.06
            sec.ena = 53.0
            sec.ek = -107.0
            sec.gbar_Ih = 0.000103457
            sec.gbar_NaV = 0.0627931
            sec.gbar_Kd = 1.39577e-08
            sec.gbar_Kv2like = 0.207064
            sec.gbar_Kv3_1 = 0.366919
            sec.gbar_K_T = 0.0410541
            sec.gbar_Im_v2 = 0.00100006
            sec.gbar_SK = 0.00534651
            sec.gbar_Ca_HVA = 0.000587526
            sec.gbar_Ca_LVA = 0.000461781
            sec.gamma_CaDynamics = 0.0012348
            sec.decay_CaDynamics = 747.87
            sec.g_pas = 0.00027801
    
    def _discretize_model(self):
        for sec in self.all:
            sec.nseg = 1 + 2 * int(sec.L / 40)

