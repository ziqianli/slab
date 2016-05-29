__author__ = 'Nelson'

from slab import *
from slab.instruments.Alazar import Alazar
from slab.experiments.ExpLib.QubitPulseSequenceExperiment import *
from numpy import mean, arange
from slab.dsfit import *


class MultimodeRabiExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_Rabi', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeRabiSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        pass

class MultimodeEFRabiExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_EF_Rabi', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeEFRabiSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        pass

class MultimodeRamseyExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_Ramsey', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeRamseySequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        print "Analyzing Ramsey Data"
        fitdata = fitdecaysin(expt_pts, expt_avg_data)

        self.offset_freq =self.cfg['multimode_ramsey']['ramsey_freq'] - fitdata[1] * 1e9

        suggested_offset_freq = self.cfg['multimodes'][int(self.cfg['multimode_ramsey']['id'])]['dc_offset_freq'] + self.offset_freq
        print "Suggested offset frequency: " + str(suggested_offset_freq)
        print "Oscillation frequency: " + str(fitdata[1] * 1e3) + " MHz"
        print "T2*: " + str(fitdata[3]) + " ns"


class MultimodeDCOffsetExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_DC_Offset_Experiment', config_file='..\\config.json', **kwargs):
        self.extra_args = {}
        for key, value in kwargs.iteritems():
            self.extra_args[key] = value

        self.amp = self.extra_args['amp']
        self.freq = self.extra_args['freq']
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeDCOffsetSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        print "Analyzing Ramsey Data"
        fitdata = fitdecaysin(expt_pts, expt_avg_data)

        self.offset_freq =self.cfg['multimode_dc_offset_experiment']['ramsey_freq'] - fitdata[1] * 1e9

        print "Flux drive amplitude: %s" %(self.amp)
        print "Offset frequency: " + str(self.offset_freq)
        print "T2*: " + str(fitdata[3]) + " ns"



class MultimodeCalibrateOffsetExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_Calibrate_Offset_Experiment', config_file='..\\config.json', **kwargs):
        self.extra_args = {}
        for key, value in kwargs.iteritems():
            self.extra_args[key] = value

        self.exp = self.extra_args['exp']
        self.mode = self.extra_args['mode']
        self.dc_offset_guess =  self.extra_args['dc_offset_guess']

        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeCalibrateOffsetSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):

        if self.exp=="multimode_rabi":
            print "Analyzing Multimode Rabi Data"
            fitdata = fitdecaysin(expt_pts[:], expt_avg_data[:])

            if (-fitdata[2]%180 - 90)/(360*fitdata[1]) < 0:
                self.flux_pi_length = (-fitdata[2]%180 + 90)/(360*fitdata[1])
                self.flux_2pi_length = (-fitdata[2]%180 + 270)/(360*fitdata[1])
                print "Flux pi length ge =" + str(self.flux_pi_length)
                print "Flux 2pi length ge =" + str(self.flux_2pi_length)
                if self.cfg['multimode_calibrate_offset_experiment'][self.exp]['save_to_file']:
                    print "writing into config file"
                    self.cfg['multimodes'][self.mode]['flux_pi_length'] =   self.flux_pi_length
                    self.cfg['multimodes'][self.mode]['flux_2pi_length'] =  self.flux_2pi_length
            else:
                # self.flux_pi_length = (-fitdata[2]%180 - 90)/(360*fitdata[1])
                # self.flux_2pi_length = (-fitdata[2]%180 + 90)/(360*fitdata[1])
                self.flux_pi_length = (-fitdata[2]%180 + 90)/(360*fitdata[1])
                self.flux_2pi_length = (-fitdata[2]%180 + 270)/(360*fitdata[1])
                print "Flux pi length ge =" + str(self.flux_pi_length)
                print "Flux 2pi length ge =" + str(self.flux_2pi_length)
                if self.cfg['multimode_calibrate_offset_experiment'][self.exp]['save_to_file']:
                    print "writing into config file"
                    self.cfg['multimodes'][self.mode]['flux_pi_length'] =   self.flux_pi_length
                    self.cfg['multimodes'][self.mode]['flux_2pi_length'] =  self.flux_2pi_length

        else:


            print "Analyzing Ramsey Data"
            fitdata = fitdecaysin(expt_pts, expt_avg_data)

            self.offset_freq =self.cfg['multimode_calibrate_offset_experiment'][self.exp]['ramsey_freq'] - fitdata[1] * 1e9
            self.suggested_dc_offset_freq = self.dc_offset_guess + self.offset_freq
            # self.suggested_dc_offset_freq = self.offset - (fitdata[1] * 1e9 - self.cfg['multimode_ramsey']['ramsey_freq'])
            print "Suggested offset frequency: " + str(self.suggested_dc_offset_freq)
            print "Oscillation frequency: " + str(fitdata[1] * 1e3) + " MHz"
            print "T2*: " + str(fitdata[3]) + " ns"
            print self.cfg['multimode_calibrate_offset_experiment'][self.exp]

            print "Saving DC offset to config for mode " + str(self.mode)
            print self.cfg['multimodes'][self.mode]['dc_offset_freq']
            self.cfg['multimodes'][self.mode]['dc_offset_freq'] = self.suggested_dc_offset_freq
            print self.cfg['multimodes'][self.mode]['dc_offset_freq']


class MultimodeQubitModeCrossKerrExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_Qubit_Mode_Cross_Kerr', config_file='..\\config.json', **kwargs):
        self.extra_args = {}
        for key, value in kwargs.iteritems():
            self.extra_args[key] = value

        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeQubitModeCrossKerrSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        pass


class MultimodeCalibrateEFSidebandExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_Calibrate_EF_Sideband_experiment', config_file='..\\config.json', **kwargs):
        self.extra_args = {}
        for key, value in kwargs.iteritems():
            self.extra_args[key] = value
        if 'mode' in self.extra_args:
            self.exp = self.extra_args['exp']
            self.mode = self.extra_args['mode']
        self.dc_offset_guess_ef =  self.extra_args['dc_offset_guess_ef']

        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeCalibrateEFSidebandSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):

        if self.exp =="multimode_ef_rabi":
            print "Analyzing EF Rabi Data"
            fitdata = fitdecaysin(expt_pts[2:], expt_avg_data[2:])

            if (-fitdata[2]%180 - 90)/(360*fitdata[1]) < 0:
                print fitdata[0]
                self.flux_pi_length_ef = (-fitdata[2]%180 + 90)/(360*fitdata[1])
                self.flux_2pi_length_ef = (-fitdata[2]%180 + 270)/(360*fitdata[1])
                print "Flux pi length EF =" + str(self.flux_pi_length_ef)
                print "Flux 2pi length EF =" + str(self.flux_2pi_length_ef)
                if self.cfg['multimode_calibrate_ef_sideband_experiment'][self.exp]['save_to_file']:
                    self.cfg['multimodes'][self.mode]['flux_pi_length_ef'] =   self.flux_pi_length_ef
                    self.cfg['multimodes'][self.mode]['flux_2pi_length_ef'] =  self.flux_2pi_length_ef
            else:
                print fitdata[0]
                # self.flux_pi_length_ef = (-fitdata[2]%180 - 90)/(360*fitdata[1])
                # self.flux_2pi_length_ef = (-fitdata[2]%180 + 90)/(360*fitdata[1])
                self.flux_pi_length_ef = (-fitdata[2]%180 + 90)/(360*fitdata[1])
                self.flux_2pi_length_ef = (-fitdata[2]%180 + 270)/(360*fitdata[1])
                print "Flux pi length EF =" + str(self.flux_pi_length_ef)
                print "Flux 2pi length EF =" + str(self.flux_2pi_length_ef)
                if self.cfg['multimode_calibrate_ef_sideband_experiment'][self.exp]['save_to_file']:
                    self.cfg['multimodes'][self.mode]['flux_pi_length_ef'] =   self.flux_pi_length_ef
                    self.cfg['multimodes'][self.mode]['flux_2pi_length_ef'] =  self.flux_2pi_length_ef

        else:

            print "Analyzing Ramsey Data"
            fitdata = fitdecaysin(expt_pts, expt_avg_data)
            self.offset_freq =self.cfg['multimode_calibrate_ef_sideband_experiment'][self.exp]['ramsey_freq'] - fitdata[1] * 1e9
            self.suggested_dc_offset_freq_ef = self.dc_offset_guess_ef + self.offset_freq
            # self.suggested_dc_offset_freq = self.offset - (fitdata[1] * 1e9 - self.cfg['multimode_ramsey']['ramsey_freq'])
            print "Suggested offset frequency: " + str(self.suggested_dc_offset_freq_ef)
            print "Oscillation frequency: " + str(fitdata[1] * 1e3) + " MHz"
            print "T2: " + str(fitdata[3]) + " ns"
            print self.cfg['multimode_calibrate_ef_sideband_experiment'][self.exp]
            print "Saving ef DC offset to config for mode " + str(self.mode)
            print self.cfg['multimodes'][self.mode]['dc_offset_freq_ef']
            self.cfg['multimodes'][self.mode]['dc_offset_freq_ef'] = self.suggested_dc_offset_freq_ef
            print self.cfg['multimodes'][self.mode]['dc_offset_freq_ef']


class MultimodeEFRamseyExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_EF_Ramsey', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeEFRamseySequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):

        print "Analyzing ef Ramsey Data"
        fitdata = fitdecaysin(expt_pts, expt_avg_data)

        self.offset_freq =self.cfg['multimode_ef_ramsey']['ramsey_freq'] - fitdata[1] * 1e9

        suggested_offset_freq = self.cfg['multimodes'][int(self.cfg['multimode_ef_ramsey']['id'])]['dc_offset_freq_ef'] - (fitdata[1] * 1e9 - self.cfg['multimode_ef_ramsey']['ramsey_freq'])
        print "Suggested offset frequency: " + str(suggested_offset_freq)
        print "Oscillation frequency: " + str(fitdata[1] * 1e3) + " MHz"
        print "T2*: " + str(fitdata[3]) + " ns"

class MultimodeRabiSweepExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_Rabi_Sweep', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeRabiSweepSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)



    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        #print self.data_file
        pass


class MultimodeEFRabiSweepExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_EF_Rabi_Sweep', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeEFRabiSweepSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)



    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        #print self.data_file
        pass


class MultimodeT1Experiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_T1', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeT1Sequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        pass


class MultimodeEntanglementExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_Entanglement', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeEntanglementSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        pass

class MultimodeGeneralEntanglementExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_General_Entanglement', config_file='..\\config.json', **kwargs):
        self.extra_args={}
        for key, value in kwargs.iteritems():
            self.extra_args[key] = value

        self.id1 = self.extra_args['id1']
        self.id2 = self.extra_args['id2']
        self.id3 = self.extra_args['id3']
        self.id4 = self.extra_args['id4']
        self.id5 = self.extra_args['id5']
        self.id6 = self.extra_args['id6']
        self.idm = self.extra_args['idm']
        self.number = self.extra_args['number']
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeGeneralEntanglementSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        self.cfg['multimode_general_entanglement']['id1'] = self.id1
        self.cfg['multimode_general_entanglement']['id2'] = self.id2
        self.cfg['multimode_general_entanglement']['id3'] = self.id3
        self.cfg['multimode_general_entanglement']['id4'] = self.id4
        self.cfg['multimode_general_entanglement']['id5'] = self.id5
        self.cfg['multimode_general_entanglement']['id6'] = self.id6
        self.cfg['multimode_general_entanglement']['number'] = self.number


class MultimodeEntanglementScalingExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_General_Entanglement', config_file='..\\config.json', **kwargs):
        self.extra_args={}
        for key, value in kwargs.iteritems():
            self.extra_args[key] = value

        self.id1 = self.extra_args['id1']
        self.id2 = self.extra_args['id2']
        self.id3 = self.extra_args['id3']
        self.id4 = self.extra_args['id4']
        self.id5 = self.extra_args['id5']
        self.id6 = self.extra_args['id6']
        self.idm = self.extra_args['idm']
        self.number = self.extra_args['number']
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeGeneralEntanglementSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        pass
        # self.cfg['multimode_general_entanglement']['id1'] = self.id1
        # self.cfg['multimode_general_entanglement']['id2'] = self.id2
        # self.cfg['multimode_general_entanglement']['id3'] = self.id3
        # self.cfg['multimode_general_entanglement']['id4'] = self.id4
        # self.cfg['multimode_general_entanglement']['id5'] = self.id5
        # self.cfg['multimode_general_entanglement']['id6'] = self.id6
        # self.cfg['multimode_general_entanglement']['number'] = self.number



class MultimodeCPhaseTestsExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_CPhase_Tests_Experiment', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeCPhaseTestsSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        pass

class MultimodeCPhaseExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_CPhase_Experiment', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeCPhaseSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        pass


class MultimodeCNOTExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_CNOT_Experiment', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeCNOTSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        pass


class MultimodePi_PiExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_Pi_Pi_Experiment', config_file='..\\config.json', **kwargs):
        if 'mode' in kwargs:
            self.id = self.extra_args['mode']
        else:
            self.id = self.cfg[self.expt_cfg_name]['id']
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodePi_PiSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        expected_period = 360.
        find_phase = 'max' #'max' or 'min'
        x_at_extremum = sin_phase(expt_pts,expt_avg_data,expected_period,find_phase)
        print 'Phase at %s: %s degrees' %(find_phase,x_at_extremum)
        self.cfg['multimodes'][self.id]['pi_pi_offset_phase'] = x_at_extremum

class Multimode_Qubit_Mode_CZ_Offset_Experiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='multimode_qubit_mode_cz_offset', config_file='..\\config.json', **kwargs):

        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=Multimode_Qubit_Mode_CZ_Offset_Sequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)
        if 'mode' in kwargs:
            self.id = self.extra_args['mode']
        else:
            self.id = self.cfg[self.expt_cfg_name]['id']

        if 'offset_exp' in self.extra_args:
            self.offset_exp = self.extra_args['offset_exp']
        else:
            self.offset_exp = self.cfg[self.expt_cfg_name]['offset_exp']


    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):

        expected_period = 360.
        if self.offset_exp==0:
            find_phase = 'max' #'max' or 'min'
            x_at_extremum = sin_phase(expt_pts,expt_avg_data,expected_period,find_phase)
            print 'Phase at %s: %s degrees' %(find_phase,x_at_extremum)
            self.cfg['multimodes'][self.id]['qubit_mode_ef_offset_0'] = x_at_extremum
        if self.offset_exp==1:
            find_phase = 'min' #'max' or 'min'
            x_at_extremum = sin_phase(expt_pts,expt_avg_data,expected_period,find_phase)
            print 'Phase at %s: %s degrees' %(find_phase,x_at_extremum)
            self.cfg['multimodes'][self.id]['qubit_mode_ef_offset_1'] = x_at_extremum


class Multimode_Qubit_Mode_CZ_V2_Offset_Experiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='multimode_qubit_mode_cz_v2_offset', config_file='..\\config.json', **kwargs):

        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=Multimode_Qubit_Mode_CZ_V2_Offset_Sequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)
        if 'mode' in kwargs:
            self.id = self.extra_args['mode']
        else:
            self.id = self.cfg[self.expt_cfg_name]['id']

        if 'offset_exp' in self.extra_args:
            self.offset_exp = self.extra_args['offset_exp']
        else:
            self.offset_exp = self.cfg[self.expt_cfg_name]['offset_exp']


    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):

        expected_period = 360.
        if self.offset_exp==0:
            find_phase = 'max' #'max' or 'min'
            x_at_extremum = sin_phase(expt_pts,expt_avg_data,expected_period,find_phase)
            print 'Phase at %s: %s degrees' %(find_phase,x_at_extremum)
            self.cfg['multimodes'][self.id]['cz_dc_phase'] = x_at_extremum

            if self.data_file:
                slab_file = SlabFile(self.data_file)
                with slab_file as f:
                    f.append_pt('offset_exp_0_phase', x_at_extremum)
                    f.close()

        if self.offset_exp==1:
            find_phase = 'min' #'max' or 'min'
            x_at_extremum = sin_phase(expt_pts,expt_avg_data,expected_period,find_phase)
            print 'Phase at %s: %s degrees' %(find_phase,x_at_extremum)
            self.cfg['multimodes'][self.id]['cz_phase'] = x_at_extremum

            if self.data_file:
                slab_file = SlabFile(self.data_file)
                with slab_file as f:
                    f.append_pt('offset_exp_1_phase', x_at_extremum)
                    f.close()

class Multimode_Mode_Mode_CZ_V2_Offset_Experiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='multimode_mode_mode_cz_v2_offset', config_file='..\\config.json', **kwargs):

        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=Multimode_Mode_Mode_CZ_V2_Offset_Sequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)
        if 'mode' in kwargs:
            self.id = self.extra_args['mode']
        else:
            self.id = self.cfg[self.expt_cfg_name]['id']

        if 'mode2' in kwargs:
            self.id2 = self.extra_args['mode2']
        else:
            self.id2 = self.cfg[self.expt_cfg_name]['id2']

        if 'offset_exp' in self.extra_args:
            self.offset_exp = self.extra_args['offset_exp']
        else:
            self.offset_exp = self.cfg[self.expt_cfg_name]['offset_exp']


    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):

        expected_period = 360.
        if self.offset_exp==0:
            find_phase = 'max' #'max' or 'min'
            x_at_extremum = sin_phase(expt_pts,expt_avg_data,expected_period,find_phase)
            print 'Phase at %s: %s degrees' %(find_phase,x_at_extremum)
            self.cfg['mode_mode_offset']['cz_dc_phase'][self.id][self.id2] = x_at_extremum

            if self.data_file:
                slab_file = SlabFile(self.data_file)
                with slab_file as f:
                    f.append_pt('2modes_offset_exp_0_phase', x_at_extremum)
                    f.close()

        if self.offset_exp==1:
            find_phase = 'min' #'max' or 'min'
            x_at_extremum = sin_phase(expt_pts,expt_avg_data,expected_period,find_phase)
            print 'Phase at %s: %s degrees' %(find_phase,x_at_extremum)
            self.cfg['mode_mode_offset']['cz_phase'][self.id][self.id2] = x_at_extremum

            if self.data_file:
                slab_file = SlabFile(self.data_file)
                with slab_file as f:
                    f.append_pt('2modes_offset_exp_1_phase', x_at_extremum)
                    f.close()


class Multimode_AC_Stark_Shift_Offset_Experiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='multimode_ac_stark_shift', config_file='..\\config.json', **kwargs):

        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=Multimode_AC_Stark_Shift_Offset_Sequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)
        if 'mode' in kwargs:
            self.id = self.extra_args['mode']
        else:
            self.id = self.cfg[self.expt_cfg_name]['id']

        if 'mode2' in kwargs:
            self.id2 = self.extra_args['mode2']
        else:
            self.id2 = self.cfg[self.expt_cfg_name]['id2']

        if 'offset_exp' in self.extra_args:
            self.offset_exp = self.extra_args['offset_exp']
        else:
            self.offset_exp = self.cfg[self.expt_cfg_name]['offset_exp']


    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):

        expected_period = 360.
        if self.offset_exp==0:
            find_phase = 'max' #'max' or 'min'
            x_at_extremum = sin_phase(expt_pts,expt_avg_data,expected_period,find_phase)
            print 'Phase at %s: %s degrees' %(find_phase,x_at_extremum)
            #self.cfg['mode_mode_offset']['cz_dc_phase'][self.id][self.id2] = x_at_extremum

            if self.data_file:
                slab_file = SlabFile(self.data_file)
                with slab_file as f:
                    f.append_pt('offset_exp_0_phase', x_at_extremum)
                    f.close()

        if self.offset_exp==1:
            find_phase = 'max' #'max' or 'min'
            x_at_extremum = sin_phase(expt_pts,expt_avg_data,expected_period,find_phase)
            print 'Phase at %s: %s degrees' %(find_phase,x_at_extremum)
            #self.cfg['mode_mode_offset']['cz_phase'][self.id][self.id2] = x_at_extremum

            if self.data_file:
                slab_file = SlabFile(self.data_file)
                with slab_file as f:
                    f.append_pt('offset_exp_1_phase', x_at_extremum)
                    f.close()

class MultimodePi_PiExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_Pi_Pi_Experiment', config_file='..\\config.json', **kwargs):

        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodePi_PiSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)
        if 'mode' in kwargs:
            self.id = self.extra_args['mode']
        else:
            self.id = self.cfg[self.expt_cfg_name]['id']

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        expected_period = 360.
        find_phase = 'max' #'max' or 'min'
        x_at_extremum = sin_phase(expt_pts,expt_avg_data,expected_period,find_phase)
        print 'Phase at %s: %s degrees' %(find_phase,x_at_extremum)
        self.cfg['multimodes'][self.id]['pi_pi_offset_phase'] = x_at_extremum


class Multimode_ef_Pi_PiExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_ef_Pi_Pi_Experiment', config_file='..\\config.json', **kwargs):

        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=Multimode_ef_Pi_PiSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)
        if 'mode_1' in kwargs:
            self.id1 = self.extra_args['mode_1']
        else:
            self.id1 = self.cfg[self.expt_cfg_name]['id1']

        if 'mode_2' in kwargs:
            self.id2 = self.extra_args['mode_2']
        else:
            self.id2 = self.cfg[self.expt_cfg_name]['id2']

    def pre_run(self):

        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        expected_period = 360.
        find_phase = 'min' #'max' or 'min'
        x_at_extremum = sin_phase(expt_pts,expt_avg_data,expected_period,find_phase)
        print 'Phase at %s: %s degrees' %(find_phase,x_at_extremum)
        self.cfg['multimodes'][self.id2]['ef_pi_pi_offset_phase'] = x_at_extremum

class Multimode_ef_2pi_Experiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_ef_2pi_Experiment', config_file='..\\config.json', **kwargs):

        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=Multimode_ef_2pi_Sequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)
        if 'mode_1' in kwargs:
            self.id1 = self.extra_args['mode_1']
        else:
            self.id1 = self.cfg[self.expt_cfg_name]['id1']

        if 'mode_2' in kwargs:
            self.id2 = self.extra_args['mode_2']
        else:
            self.id2 = self.cfg[self.expt_cfg_name]['id2']

    def pre_run(self):

        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        expected_period = 360.
        find_phase = 'min' #'max' or 'min'
        x_at_extremum = sin_phase(expt_pts,expt_avg_data,expected_period,find_phase)
        print 'Phase at %s: %s degrees' %(find_phase,x_at_extremum)
        self.cfg['multimodes'][self.id2]['ef_2pi_offset_phase'] = x_at_extremum



class CPhaseOptimizationSweepExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='multimode_cphase_optimization_sweep', config_file='..\\config.json', **kwargs):
        self.extra_args={}
        for key, value in kwargs.iteritems():
            self.extra_args[key] = value
        self.idle_time = self.extra_args['idle_time']
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=CPhaseOptimizationSweepSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        slab_file = SlabFile(self.data_file)
        with slab_file as f:
            f.append_pt('idle_time', self.idle_time)
            f.append_line('sweep_expt_avg_data', expt_avg_data)
            f.append_line('sweep_expt_pts', expt_pts)

            f.close()

class MultimodeSingleResonatorTomography(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='multimode_Single_Resonator_Tomography', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeSingleResonatorTomographySequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        pass

class MultimodeSingleResonatorRandomizedBenchmarkingExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='multimode_single_resonator_randomized_benchmarking', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeSingleResonatorRandomizedBenchmarkingSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        pass

class MultimodeQubitModeRandomizedBenchmarkingExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='multimode_qubit_mode_randomized_benchmarking', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeQubitModeRandomizedBenchmarkingSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        pass


class MultimodeTwoResonatorTomography(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='multimode_two_Resonator_Tomography', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeTwoResonatorTomographySequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        pass

class MultimodeTwoResonatorTomographyPhaseSweepExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='multimode_two_resonator_tomography_phase_sweep', config_file='..\\config.json', **kwargs):
        self.extra_args={}
        for key, value in kwargs.iteritems():
            self.extra_args[key] = value
        self.tomography_num = self.extra_args['tomography_num']

        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeTwoResonatorTomographyPhaseSweepSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        pass


class MultimodeThreeModeCorrelationExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='multimode_three_mode_correlation_experiment', config_file='..\\config.json', **kwargs):
        # self.extra_args={}
        # for key, value in kwargs.iteritems():
        #     self.extra_args[key] = value
        # self.tomography_num = self.extra_args['tomography_num']

        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeThreeModeCorrelationSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        pass

class MultimodeCPhaseAmplificationExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_CPhase_Amplification_Experiment', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeCPhaseAmplificationSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        pass


class MultimodeCNOTAmplificationExperiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_CNOT_Amplification_Experiment', config_file='..\\config.json', **kwargs):
        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=MultimodeCNOTAmplificationSequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):
        pass


class Multimode_State_Dep_Shift_Experiment(QubitPulseSequenceExperiment):
    def __init__(self, path='', prefix='Multimode_State_Dep_Shift', config_file='..\\config.json', **kwargs):

        self.extra_args={}
        for key, value in kwargs.iteritems():
            self.extra_args[key] = value
        self.mode = self.extra_args['mode']
        self.exp = self.extra_args['exp']
        self.qubit_shift_ge = self.extra_args['qubit_shift_ge']
        self.qubit_shift_ef = self.extra_args['qubit_shift_ef']

        QubitPulseSequenceExperiment.__init__(self, path=path, prefix=prefix, config_file=config_file,
                                                    PulseSequence=Multimode_State_Dep_Shift_Sequence, pre_run=self.pre_run,
                                                    post_run=self.post_run, prep_tek2= True,**kwargs)

    def pre_run(self):
        self.tek2 = InstrumentManager()["TEK2"]

    def post_run(self, expt_pts, expt_avg_data):

        if self.exp == 1 or self.exp==2:

            print "Analyzing Rabi Data"

            xdata = expt_pts
            ydata = expt_avg_data
            FFT=scipy.fft(ydata)
            fft_freqs=scipy.fftpack.fftfreq(len(ydata),xdata[1]-xdata[0])
            max_ind=np.argmax(abs(FFT[2:len(ydata)/2.]))+2
            fft_val=FFT[max_ind]

            fitparams=[0,0,0,0,0]
            fitparams[4]=np.mean(ydata)
            fitparams[0]=(max(ydata)-min(ydata))/2.#2*abs(fft_val)/len(fitdatay)
            fitparams[1]=fft_freqs[max_ind]
            fitparams[2]=-90.0
            fitparams[3]=(max(xdata)-min(xdata))
            fitdata=fitdecaysin(xdata[:],ydata[:],fitparams=fitparams,showfit=False)

            self.pi_length = around(1/fitdata[1]/2,decimals=2)
            self.half_pi_length =around(1/fitdata[1]/4,decimals=2)

            if self.qubit_shift_ge == 1:
                print 'Rabi pi: %s ns' % (self.pi_length)
                print 'Rabi pi/2: %s ns' % (self.half_pi_length)
                print 'T1*: %s ns' % (fitdata[3])
            elif self.qubit_shift_ef == 1:
                print 'Rabi ef pi: %s ns' % (self.pi_length)
                print 'Rabi ef pi/2: %s ns' % (self.half_pi_length)
                print 'T1*: %s ns' % (fitdata[3])

        elif self.exp == 6:
            print "Analyzing EF Rabi Data"
            fitdata = fitdecaysin(expt_pts[2:], expt_avg_data[2:])

            if (-fitdata[2]%180 - 90)/(360*fitdata[1]) < 0:
                print fitdata[0]
                self.flux_pi_length_ef = (-fitdata[2]%180 + 90)/(360*fitdata[1])
                self.flux_2pi_length_ef = (-fitdata[2]%180 + 270)/(360*fitdata[1])
                print "Flux pi length EF =" + str(self.flux_pi_length_ef)
                print "Flux 2pi length EF =" + str(self.flux_2pi_length_ef)


        elif self.exp == 3 or self.exp ==4 or self.exp ==5:

            print "Analyzing offset phase in presence of photon in mode %s" %(self.mode)

            xdata = expt_pts
            ydata = expt_avg_data
            fitparams = [(max(ydata)-min(ydata))/(2.0),1/360.0,90,mean(ydata)]
            fitdata=fitsin(xdata[:],ydata[:],fitparams=fitparams,showfit=False)
            if self.exp == 3:
                self.cfg['multimodes'][self.mode]['qubit_offset_phase'] = around((-(fitdata[2]%180) + 90),2)
                print "Offset Phase = %s" %(self.cfg['multimodes'][self.mode]['qubit_offset_phase'])
            elif self.exp ==4:
                self.cfg['multimodes'][self.mode]['qubit_offset_phase_2'] = around((-(fitdata[2]%180) + 90),2)
                print "Offset Phase = %s" %(self.cfg['multimodes'][self.mode]['qubit_offset_phase_2'])
            else:
                print "Offset Phase = %s" %(around((-(fitdata[2]%180) + 90),2))

        else:

            print "Analyzing Ramsey Data"
            fitdata = fitdecaysin(expt_pts, expt_avg_data)

            self.offset_freq =self.cfg['multimode_state_dep_shift']['ramsey_freq'] - fitdata[1] * 1e9


            print "State dependent shift = " + str(self.offset_freq) + "MHz"
            print "Oscillation frequency: " + str(fitdata[1] * 1e3) + " MHz"
            print "T2*: " + str(fitdata[3]) + " ns"

            if self.qubit_shift_ge == 1:
                self.cfg['multimodes'][self.mode]['shift'] =   self.offset_freq
            elif self.qubit_shift_ef ==1:
                self.cfg['multimodes'][self.mode]['shift_ef'] =   self.offset_freq