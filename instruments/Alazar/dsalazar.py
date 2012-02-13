# -*- coding: utf-8 -*-
"""
Created on Tue Jun 07 15:01:07 2011

@author: Phil
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 17:14:11 2011

@author: Phil
"""
import ctypes as C
import numpy as np
import sys
from slablayout import *
from guiqwt.pyplot import *

#import matplotlib.pyplot as mplt
#import operator

U8 = C.c_uint8
U8P = C.POINTER(U8)
U32 = C.c_uint32
U32P = C.POINTER(U32)
U32PP = C.POINTER(U32P)

DEBUGALAZAR=False

#try:
#    CTHelp = C.CDLL(r'C:\Users\Phil\Desktop\AlazarApi\trunk\Debug\ctypes_help.dll')
#except:
#    print "Couldn't load ctypes_help.dll"

# Helper Functions
def int_linterp(x, a1, a2, b1, b2):
    'Moves x from interval [a1, a2] to interval [b1, b2]'
    return int(b1 + ((x - a1) * (b2 - b1)) / float((a2 - a1)))

def ret_to_str(retCode, Az):
    Az.AlazarErrorToText.restype = C.c_char_p
    return Az.AlazarErrorToText(U32(retCode))   

class AlazarConstants():
    # Clock Constants
    clock_source = {"internal" : U32(1),
              "reference": U32(7),
              "60 MHz" : U32(4),
              "1 GHz" : U32(5)}
    sample_rate = [(1,U32(1)), (2,U32(2)), (5,U32(4)), (10,U32(8)), (20,U32(10)),
            (50,U32(12)), (100,U32(14)), (200,U32(16)), (500,U32(18)), (1000,U32(20)),
            (2000,U32(24)), (5000,U32(26)), (10000,U32(28)), (20000,U32(30)), (50000,U32(34)),
            (100000,U32(36)), (250000,U32(43)), (500000,U32(48)), (1000000,U32(53))]
#    sample_rate_txt = {"1 kHz":U32(1),"2 kHz":U32(2),"5 kHz":U32(4),"10 kHz":U32(8),"20 kHz":U32(10),
#                      "100 kHz": U32(14),"200 kHz": U32(16),"500 kHz":U32(18),
#                      "1 MHz":U32(20),"2 MHz":U32(24),"5 MHz":U32(26),"10 MHz":U32(28),
#                      "20 MHz":U32(30),"50 MHz":U32(34),
#                      "100 MHz":U32(36),"250 MHz":U32(43),"500 MHz":U32(48),"1 GHz":U32(53)}
    sample_rate_txt = {"1 kHz":1,"2 kHz":2,"5 kHz":5,"10 kHz":10,"20 kHz":20,
                      "100 kHz": 100,"200 kHz": 200,"500 kHz":500,
                      "1 MHz":1000,"2 MHz":2000,"5 MHz":5000,"10 MHz":10000,
                      "20 MHz":20000,"50 MHz":50000,"100 MHz":100000,
                      "250 MHz":250000,"500 MHz":500000,"1 GHz":1000000}
    sample_rate_external = U32(64)
    sample_rate_reference = U32(1000000000)
    clock_edge = {"rising": U32(0),
                  "falling": U32(1)}
    
    # Trigger Constants
    trigger_source = {"CH_A":U32(0), "CH_B":U32(1), "external":U32(2), "disabled":U32(3)}
    trigger_operation = {"or":U32(2), "and":U32(3), "xor":U32(4), "and not":U32(5)}
    trigger_ext_coupling = {"AC":U32(1), "DC":U32(2)}
    trigger_single_op = U32(0)
    trigger_engine_1 = U32(0)
    trigger_engine_2 = U32(1)
    trigger_edge = {"rising":U32(1), "falling":U32(2)}

    # Channel Constants     
    channel = {"CH_A":U8(1), "CH_B":U8(2)}
    input_coupling = {"AC":U32(1), "DC":U32(2)}
    input_range = [(0.04,U32(2)), (0.1,U32(5)), (0.2,U32(6)), (0.4,U32(6)),
                   (1,U32(10)), (2,U32(11)), (4,U32(12))]
    input_range_txt = {"40 mV":0.04,"100 mV":0.1,"200 mV":0.2,"400 mV":0.4,
                       "1 V":1.0,"2 V":2.0,"4 V":4.0}
    input_filter = {False:U32(0), True:U32(1)}
    
class AlazarConfig1():
    _form_fields_ =[("samplesPerRecord","Samples",2048),
                    ("recordsPerBuffer","Records per Buffer",10),
                    ("recordsPerAcquisition","Total Records",10),
                    ("bufferCount","Number of Buffers",1),
                    ("clock_source","Clock Source", ["internal",("internal","internal"),("reference","reference"),("60 MHz","60 MHz"),("1 GHz","1 GHz")]),
                    ("clock_edge","Clock Edge", ["rising",("rising","Rising"),("falling","Falling")]),
                    ("sample_rate", "Sample Rate", [1000,(1,"1 kHz"),(2, "2 kHz"),(5,"5 kHz"),(10,"10 kHz"),(20,"20 kHz"),(1000,"1 MHz"),(2000,"2 MHz"),(5000, "5 MHz"),(10000,"10 MHz"),(20000,"20 MHz"),(50000, "50 MHz"),(100000, "100 MHz"),(250000,"250 MHz"),(500000,"500 MHz"),(1000000,"1 GHz")]),
                    ("trigger_source1","Trigger Source 1", ["CH_A", ("CH_A", "Channel 1"),("CH_B", "Channel 2"),("external","External"),("disabled","Disabled")]),
                    ("trigger_edge1", "Trigger Edge 1",["rising",("rising","Rising"),("falling","Falling")]),
                    ("trigger_level1", "Trigger Level 1", 0),
                    ("trigger_source2","Trigger Source 2", ["disabled", ("CH_A", "Channel 1"),("CH_B", "Channel 2"),("external","External"),("disabled","Disabled")]),
                    ("trigger_edge2", "Trigger Edge 2", ["rising", ("rising","Rising"),("falling","Falling")]),
                    ("trigger_level2", "Trigger Level 2", 0),
                    ("trigger_operation", "Trigger Operation", ["or",("or","OR"), ("and","AND"),("xor","XOR"),("and not","AND NOT")]),
                    ("trigger_coupling", "Trigger Coupling", ["DC",("DC","DC"),("AC","AC")]),
                    ("timeout","Timeout",5000),
                    ("ch1_enabled","Ch1 Enabled", True),
                    ("ch1_coupling","Ch1 Coupling", ["DC",("DC","DC"),("AC","AC")]),
                    ("ch1_range","Ch1 Range", [1,(0.04,"40 mV"),(0.1,"100 mV"),(0.2,"200 mV"),(0.4,"400 mV"),(1, "1 V"),(2,"2 V"),(4,"4 V")]),
                    ("ch1_filter","Ch1 Filter",False),
                    ("ch2_enabled","Ch2 Enabled", False),
                    ("ch2_coupling","Ch2 Coupling", ["DC",("DC","DC"),("AC","AC")]),
                    ("ch2_range","Ch2 Range", [1,(0.04,"40 mV"),(0.1,"100 mV"),(0.2,"200 mV"),(0.4,"400 mV"),(1, "1 V"),(2,"2 V"),(4,"4 V")]),
                    ("ch2_filter","Ch2 Filter",False),
                   ]
    
    def __init__(self,config_dict=None):
        if config_dict is not None:
            self.from_dict(config_dict)
            
    def from_dict(self,config_dict):
        for k,v in config_dict.items():
            self.__dict__[k]=v
        
    def get_formdata (self):
        fd=[]
        for field_name,field_label,field_value in self._form_fields_:
            if isinstance(field_value,(list,tuple)):
                field_value[0]=self.__dict__[field_name]
            else:
                field_value=self.__dict__[field_name]
            fd.append((field_name,field_name,field_value))
        return fd

    def get_dict(self):
        d={}
        for field_name in type(self)._form_fields_:
            d[field_name]=self.__getattribute__(field_name)
        return d       

class AlazarConfig():
    _fields_ = [ 'samplesPerRecord',
                 'recordsPerBuffer',
                 'recordsPerAcquisition',
                 'bufferCount',
                 'clock_source',
                 'clock_edge',
                 'sample_rate',
                 'trigger_source1',
                 'trigger_edge1',
                 'trigger_level1',
                 'trigger_source2',
                 'trigger_edge2',
                 'trigger_level2',
                 'trigger_operation',
                 'trigger_coupling',
                 'timeout',
                 'ch1_enabled',
                 'ch1_coupling',
                 'ch1_range',
                 'ch1_filter',
                 'ch2_enabled',
                 'ch2_coupling',
                 'ch2_range',
                 'ch2_filter']
    
    def __init__(self,config_dict=None):
        if config_dict is not None:
            self.from_dict(config_dict)
            
    def from_dict(self,config_dict):
        for k,v in config_dict.items():
            self.__dict__[k]=v
        
    def get_dict(self):
        d={}
        for field_name in self._fields_:
            d[field_name]=getattr(self,field_name)
        return d       
        
    def from_form(self,widget):
        self.samplesPerRecord = widget.samplesSpinBox.value()
        self.recordsPerBuffer = widget.recordsSpinBox.value()
        self.bufferCount = widget.buffersSpinBox.value()
        self.recordsPerAcquisition = max(self.recordsPerBuffer,widget.recordsPerAcquisitionSpinBox.value())
        self.clock_source = str(widget.clocksourceComboBox.currentText())
        self.clock_edge = str(widget.clockedgeComboBox.currentText())
        self.sample_rate = AlazarConstants.sample_rate_txt[str(widget.samplerateComboBox.currentText())]
        self.trigger_source1 = str(widget.trig1_sourceComboBox.currentText())
        self.trigger_edge1 = str(widget.trig1_edgeComboBox.currentText())
        self.trigger_level1 = widget.trig1_levelSpinBox.value()
        self.trigger_source2 = str(widget.trig2_sourceComboBox.currentText())
        self.trigger_edge2 = str(widget.trig2_edgeComboBox.currentText())
        self.trigger_level2 = widget.trig2_levelSpinBox.value()

        self.trigger_operation = str(widget.trigOpComboBox.currentText())
        self.trigger_coupling = str(widget.trigCouplingComboBox.currentText())

        self.timeout = widget.timeoutSpinBox.value()

        self.ch1_enabled = widget.ch1_enabledCheckBox.isChecked()
        self.ch1_coupling = str(widget.ch1_couplingComboBox.currentText())
        self.ch1_range = AlazarConstants.input_range_txt[str(widget.ch1_rangeComboBox.currentText())]
        self.ch1_filter = widget.ch1_filteredCheckBox.isChecked()

        self.ch2_enabled = widget.ch2_enabledCheckBox.isChecked()
        self.ch2_coupling = str(widget.ch2_couplingComboBox.currentText())
        self.ch2_range = AlazarConstants.input_range_txt[str(widget.ch2_rangeComboBox.currentText())]
        self.ch2_filter = widget.ch2_filteredCheckBox.isChecked()
        
def round_samples(x, base=64):
    return int(base * round(float(x)/base))

class Alazar():
    def __init__(self,config=None, handle=None):
        self.Az = C.CDLL(r'C:\Windows\SysWow64\ATSApi.dll')
        if config is None:
            self.config = AlazarConfig()
        else:
            self.config = config
            
        if handle:
            self.handle = handle
        else:
            self.handle = self.get_handle()
        if not self.handle:
            raise RuntimeError("Board could not be found")
            
    def get_handle(self):
        return self.Az.AlazarGetBoardBySystemID(U32(1), U32(1))
        
    def configure(self,config=None):
        if config is not None: self.config=config
        if self.config.samplesPerRecord<256 or (self.config.samplesPerRecord  % 64)!=0:
            print "Warning! invalid samplesPerRecord!"
            print "Frames will not align properly!"
            print "Try %d or %d" % (max(256,self.config.samplesPerRecord-(self.config.samplesPerRecord  % 64)),
                                                                 max(256,self.config.samplesPerRecord+64-(self.config.samplesPerRecord  % 64)))
            
        if DEBUGALAZAR: print "Configuring Clock"
        self.configure_clock()
        if DEBUGALAZAR: print "Configuring triggers"
        self.configure_trigger()
        if DEBUGALAZAR: print "Configuring inputs"
        self.configure_inputs()
        if DEBUGALAZAR: print "Configuring buffers"
        self.configure_buffers()
           
    def configure_clock(self, source=None, rate=None, edge=None):
        """
        @param source: 'internal' to use internal clock with rate specified by
        rate parameter. '60 MHz' for external clock with rate <= 60 MHz.
        '1 GHz' for external clock with rate <= 1 GHz.
        'reference' --> see Alazar documentation for AlazarSetCaptureClock
        
        @param rate: Rate (in KHz) for the internal clock, ignored for external
        This will be rounded down to closest value specified by AlazarSetCaptureClock
        documentation
        
        @param edge: 'rising' or 'falling'
        """
        if source is not None: self.config.clock_source= source        
        if rate is not None: self.config.clock_rate = rate   #check this to make sure it's behaving properly
        if edge is not None: self.config.edge = edge 
        

        #convert clock config
        if self.config.clock_source not in ["internal", "external", "reference"]:
            raise ValueError("source must be one of internal, external, or reference")
        if self.config.clock_edge not in ["rising", "falling"]:
            raise ValueError("edge must be one of rising or falling")

        if self.config.clock_source == "internal":
            source = AlazarConstants.clock_source["internal"]
            for (rate, value) in AlazarConstants.sample_rate:
                if rate >= self.config.sample_rate:
                    if rate > self.config.sample_rate:
                        print "Warning: sample_rate not found. Using first smaller value", rate, "Khz"
                        self.config.sample_rate = rate
                    sample_rate = value
                    break
        elif self.config.clock_source == "external":
            sample_rate = AlazarConstants.sample_rate_external
            if self.config.sample_rate < 60000:
                source = AlazarConstants.source["60 MHz"]
            elif self.config.sample_rate < 1000000:
                source = AlazarConstants.source["1 GHz"]
            else:
                raise ValueError("Not supported (yet?)")
        else:
            raise ValueError("reference signal not implemented yet")
        ret = self.Az.AlazarSetCaptureClock(self.handle, source, sample_rate, AlazarConstants.clock_edge[self.config.clock_edge], U32(0))
        if DEBUGALAZAR: print "ClockConfig:", ret_to_str(ret, self.Az)

    def configure_trigger(self,source=None, source2=None, edge=None, edge2=None,
                 level=None, level2=None, operation=None, coupling=None, timeout=None):
        """
        Can set up to two trigger operations to be performed
        @param source: Where the first trigger engine should take its input.
        'CH_A' for channel A, 'CH_B' for channel B, "external" for external source,
        'disabled' to disable trigger engine
        
        @param edge: 'rising' or 'falling'
        
        @param level: integer in interval [-100, 100], i.e. a percent of the input range
        at which to trigger a capture
        
        @param coupling: 'AC' or 'DC'
        
        @param operation: How to combine two enabled triggers to generate capture events
        'or' to trigger on either engine, 'and' to trigger only when both go high,
        'xor', 'and not' offered as well.
        
        @param timeout: How to 
        """
        if source is not None: self.config.trigger_source1 = source
        if source2 is not None: self.config.trigger_source2 = source2
        if edge is not None: self.config.trigger_edge1 = edge
        if edge2 is not None: self.config.trigger_edge2 = edge2
        if level is not None: self.config.trigger_level1 = level
        if level2 is not None: self.config.trigger_level2 = level2
        
        if not (self.config.trigger_level1 >= -100 and self.config.trigger_level1 < 100):
            raise ValueError("Level must be value in [-100,100]")
        if not (self.config.trigger_level2 >= -100 and self.config.trigger_level2 < 100):
            raise ValueError("Level must be value in [-100,100]")
        if operation is not None: self.config.trigger_operation = operation
        if coupling is not None: self.config.trigger_coupling= coupling
        if timeout is not None: self.config.timeout= timeout
        
        if source2 == "disabled":
            op = AlazarConstants.single_op
        else:
            op = AlazarConstants.trigger_operation[self.config.trigger_operation]

        ret = self.Az.AlazarSetTriggerOperation(self.handle, op,
                AlazarConstants.trigger_engine_1, AlazarConstants.trigger_source[self.config.trigger_source1], AlazarConstants.trigger_edge[self.config.trigger_edge1], U32(int_linterp(self.config.trigger_level1, -100, 100, 0, 255)),
                AlazarConstants.trigger_engine_2, AlazarConstants.trigger_source[self.config.trigger_source2], AlazarConstants.trigger_edge[self.config.trigger_edge2], U32(int_linterp(self.config.trigger_level1, -100, 100, 0, 255)))
        if DEBUGALAZAR: print "Set Trigger:", ret_to_str(ret, self.Az)
        if self.config.trigger_source1 == "external":
            ret = self.Az.AlazarSetExternalTrigger(self.handle, AlazarConstants.trigger_ext_coupling[self.config.trigger_coupling], U32(0))
            if DEBUGALAZAR: print "Set External Trigger:", ret_to_str(ret, self.Az)
        
    def configure_inputs(self, enabled1=None, coupling1=None, range1=None, filter1=None, enabled2=None, coupling2=None, range2=None, filter2=None):
        """
        @param channel: 'CH_A' or 'CH_B'. Create two InputConfig classes for both
        
        @param coupling: 'AC' or 'DC'
        
        @param input_range: Input range in volts. rounds down to the closest value
        provided by AlazarInputControl
        
        @param filter_above_20MHz: if True, enable the 20MHz BW filter
        """
        
        if enabled1 is not None: self.config.ch1_enabled = enabled1
        if coupling1 is not None: self.config.ch1_coupling= coupling1
        if range1 is not None: self.config.ch1_range = range1
        if filter1 is not None: self.config.ch1_filter

        if enabled2 is not None: self.config.ch2_enabled = enabled2
        if coupling2 is not None: self.config.ch2_coupling= coupling2
        if range2 is not None: self.config.ch2_range = range2
        if filter2 is not None: self.config.ch2_filter
        
        for (voltage, value) in AlazarConstants.input_range:
            if self.config.ch1_range <= voltage:
                if self.config.ch1_range < voltage:
                    if DEBUGALAZAR: print "Warning: input range not found, using closest value,", voltage, "Volts"
                self.config.ch1_range = voltage
                ch1_range_value=value
                break
        for (voltage, value) in AlazarConstants.input_range:
            if self.config.ch2_range <= voltage:
                if self.config.ch2_range < voltage:
                    if DEBUGALAZAR: print "Warning: input range not found, using closest value,", voltage, "Volts"
                self.config.ch2_range = voltage
                ch2_range_value=value
                break

        if self.config.ch1_enabled:  
            ret = self.Az.AlazarInputControl(self.handle, AlazarConstants.channel["CH_A"], AlazarConstants.input_coupling[self.config.ch1_coupling], ch1_range_value, U32(2))
            if DEBUGALAZAR: print "Input Control CH1:", ret_to_str(ret, self.Az)
            ret = self.Az.AlazarSetBWLimit(self.handle, AlazarConstants.channel["CH_A"], AlazarConstants.input_filter[self.config.ch1_filter])
            if DEBUGALAZAR: print "Set BW Limit:", ret_to_str(ret, self.Az)
        if self.config.ch2_enabled:  
            ret = self.Az.AlazarInputControl(self.handle, AlazarConstants.channel["CH_B"], AlazarConstants.input_coupling[self.config.ch2_coupling], ch2_range_value, U32(2))
            if DEBUGALAZAR: print "Input Control CH1:", ret_to_str(ret, self.Az)
            ret = self.Az.AlazarSetBWLimit(self.handle, AlazarConstants.channel["CH_B"], AlazarConstants.input_filter[self.config.ch2_filter])
            if DEBUGALAZAR: print "Set BW Limit:", ret_to_str(ret, self.Az)


    def configure_buffers(self,samplesPerRecord=None,recordsPerBuffer=None,recordsPerAcquisition=None,bufferCount=None):
        if samplesPerRecord is not None: self.config.samplesPerRecord=samplesPerRecord
        if recordsPerBuffer is not None: self.config.recordsPerBuffer=recordsPerBuffer
        if recordsPerAcquisition is not None: self.config.recordsPerAcquisition=recordsPerAcquisition
        if bufferCount is not None: self.config.bufferCount = bufferCount
        
        self.config.channelCount=0
        channel=0        #Create channel flag
        if self.config.ch1_enabled: 
            channel= channel | 1
            self.config.channelCount+=1
        if self.config.ch2_enabled: 
            channel= channel | 2
            self.config.channelCount+=1
        
        pretriggers=C.c_long(0) #no pretriggering support for now
        flags = U32 (513) #ADMA flags, should update to be more general
        
        ret = self.Az.AlazarSetRecordSize(self.handle,U32(0),U32(self.config.samplesPerRecord))        
        if DEBUGALAZAR: print "Set Record Size:", ret_to_str(ret,self.Az)
        
        ret = self.Az.AlazarBeforeAsyncRead(self.handle,U32(channel),pretriggers,
                                       U32(self.config.samplesPerRecord), 
                                       U32(self.config.recordsPerBuffer),
                                       U32(self.config.recordsPerAcquisition),
                                       flags)
        if DEBUGALAZAR: print "Before Read:", ret_to_str(ret,self.Az)

        self.config.bytesPerBuffer=(self.config.samplesPerRecord * self.config.recordsPerBuffer * self.config.channelCount)        
        self.bufs=[]
        buftype=U8 * self.config.bytesPerBuffer
        for i in range(self.config.bufferCount):
            self.bufs.append(buftype())            
            for j in range(self.config.bytesPerBuffer):
                self.bufs[i][j]=U8(0)
            #ret = self.Az.AlazarPostAsyncBuffer(self.handle,self.bufs[i],U32(self.config.bytesPerBuffer))
        if DEBUGALAZAR: print "Posted buffers: ", ret_to_str(ret,self.Az)
        self.arrs=[np.ctypeslib.as_array(b) for b in self.bufs]
#        for a in self.arrs:
#            for i in range(a.__len__()):
#                a[i]=0

    def post_buffers(self):
        self.config.channelCount=0
        channel=0        #Create channel flag
        if self.config.ch1_enabled: 
            channel= channel | 1
            self.config.channelCount+=1
        if self.config.ch2_enabled: 
            channel= channel | 2
            self.config.channelCount+=1

        pretriggers=C.c_long(0) #no pretriggering support for now
        flags = U32 (513) #ADMA flags, should update to be more general
            
        ret = self.Az.AlazarBeforeAsyncRead(self.handle,U32(channel),pretriggers,
                                       U32(self.config.samplesPerRecord), 
                                       U32(self.config.recordsPerBuffer),
                                       U32(self.config.recordsPerAcquisition),
                                       flags)
        for i in range (self.config.bufferCount):
            ret = self.Az.AlazarPostAsyncBuffer(self.handle,self.bufs[i],U32(self.config.bytesPerBuffer))

    def acquire_data(self):
        self.post_buffers()
        #self.avg_data=np.zeros(self.config.samplesPerRecord * self.config.recordsPerBuffer * self.config.channelCount,dtype=float)
        buffersCompleted=0
        buffersPerAcquisition=self.config.recordsPerAcquisition/self.config.recordsPerBuffer
        ret = self.Az.AlazarStartCapture(self.handle)
        if DEBUGALAZAR: print "Start Capture: ", ret_to_str(ret,self.Az)
        if DEBUGALAZAR: print "Buffers per Acquisition: ", buffersPerAcquisition
        while (buffersCompleted < buffersPerAcquisition):
            if DEBUGALAZAR: print "Waiting for buffer ", buffersCompleted
            buf_idx = buffersCompleted % self.config.bufferCount
            buffersCompleted+=1           
            ret = self.Az.AlazarWaitAsyncBufferComplete(self.handle,self.bufs[buf_idx],U32(self.config.timeout))
            if DEBUGALAZAR: print "WaitAsyncBuffer: ", ret_to_str(ret,self.Az)            
            if ret_to_str(ret,self.Az) == "ApiWaitTimeout":
                ret = self.Az.AlazarAbortAsyncRead(self.handle)
                if DEBUGALAZAR: print "Abort AsyncRead: ", ret_to_str(ret,self.Az)            
                break
            if buffersCompleted < buffersPerAcquisition:            
                ret = self.Az.AlazarPostAsyncBuffer(self.handle,self.bufs[buf_idx],U32(self.config.bytesPerBuffer))
                if DEBUGALAZAR: print "PostAsyncBuffer: ", ret_to_str(ret,self.Az)            
            #self.avg_data+=self.arrs[buf_idx]
        #self.avg_data=self.avg_data/buffersCompleted
        ret = self.Az.AlazarAbortAsyncRead(self.handle)

    def acquire_avg_data(self, excise=None):
        self.post_buffers()
        self.avg_data=np.zeros(self.config.samplesPerRecord * self.config.recordsPerBuffer * self.config.channelCount,dtype=long)
        buffersCompleted=0
        buffersPerAcquisition=self.config.recordsPerAcquisition/self.config.recordsPerBuffer
        ret = self.Az.AlazarStartCapture(self.handle)
        if DEBUGALAZAR: print "Start Capture: ", ret_to_str(ret,self.Az)
        if DEBUGALAZAR: print "Buffers per Acquisition: ", buffersPerAcquisition
        while (buffersCompleted < buffersPerAcquisition):
            if DEBUGALAZAR: print "Waiting for buffer ", buffersCompleted
            buf_idx = buffersCompleted % self.config.bufferCount
            buffersCompleted+=1           
            ret = self.Az.AlazarWaitAsyncBufferComplete(self.handle,self.bufs[buf_idx],U32(self.config.timeout))
            if DEBUGALAZAR: print "WaitAsyncBuffer: ", ret_to_str(ret,self.Az)            
            if ret_to_str(ret,self.Az) == "ApiWaitTimeout":
                ret = self.Az.AlazarAbortAsyncRead(self.handle)
                if DEBUGALAZAR: print "Abort AsyncRead: ", ret_to_str(ret,self.Az)            
                break
            self.avg_data+=self.arrs[buf_idx]
            #plot(self.arrs[buf_idx])
            if buffersCompleted < buffersPerAcquisition:            
                ret = self.Az.AlazarPostAsyncBuffer(self.handle,self.bufs[buf_idx],U32(self.config.bytesPerBuffer))
                if DEBUGALAZAR: print "PostAsyncBuffer: ", ret_to_str(ret,self.Az)            
        self.avg_data=self.avg_data/buffersCompleted
        ret = self.Az.AlazarAbortAsyncRead(self.handle)
        if (self.config.ch1_enabled) and (self.config.ch2_enabled):
            ch1_pts=(np.array(self.avg_data[:self.config.samplesPerRecord])-128.)*(self.config.ch1_range/128.)
            ch2_pts=(np.array(self.avg_data[self.config.samplesPerRecord:])-128.)*(self.config.ch2_range/128.)
        elif (self.config.ch1_enabled):
            ch1_pts=(np.array(self.avg_data)-128.)*(self.config.ch1_range/128.)
            ch2_pts=np.zeros(len(ch1_pts))
        else: return None,None
        tpts=np.arange(self.config.samplesPerRecord)/float(self.config.sample_rate*1e3)
        if excise is not None:
            return tpts[excise[0]:excise[1]],ch1_pts[excise[0]:excise[1]],ch2_pts[excise[0]:excise[1]]
        else:
            return tpts,ch1_pts,ch2_pts
            
    def acquire_avg_data2(self, excise=None):
        self.post_buffers()
        self.avg_data=np.zeros(self.config.samplesPerRecord * self.config.channelCount,dtype=float)
        buffersCompleted=0
        buffersPerAcquisition=self.config.recordsPerAcquisition/self.config.recordsPerBuffer
        ret = self.Az.AlazarStartCapture(self.handle)
        if DEBUGALAZAR: print "Start Capture: ", ret_to_str(ret,self.Az)
        if DEBUGALAZAR: print "Buffers per Acquisition: ", buffersPerAcquisition
        while (buffersCompleted < buffersPerAcquisition):
            if DEBUGALAZAR: print "Waiting for buffer ", buffersCompleted
            buf_idx = buffersCompleted % self.config.bufferCount
            buffersCompleted+=1           
            ret = self.Az.AlazarWaitAsyncBufferComplete(self.handle,self.bufs[buf_idx],U32(self.config.timeout))
            if DEBUGALAZAR: print "WaitAsyncBuffer: ", ret_to_str(ret,self.Az)            
            if ret_to_str(ret,self.Az) == "ApiWaitTimeout":
                ret = self.Az.AlazarAbortAsyncRead(self.handle)
                if DEBUGALAZAR: print "Abort AsyncRead: ", ret_to_str(ret,self.Az)            
                break
            for n in range(self.config.recordsPerBuffer):                
                self.avg_data+=self.arrs[buf_idx][n*self.config.recordsPerBuffer:n*self.config.recordsPerBuffer+self.config.samplesPerRecord* self.config.channelCount]
            #plot(self.arrs[buf_idx])
            if buffersCompleted < buffersPerAcquisition:            
                ret = self.Az.AlazarPostAsyncBuffer(self.handle,self.bufs[buf_idx],U32(self.config.bytesPerBuffer))
                if DEBUGALAZAR: print "PostAsyncBuffer: ", ret_to_str(ret,self.Az)            
        self.avg_data=self.avg_data/buffersCompleted/self.config.recordsPerAcquisition
        ret = self.Az.AlazarAbortAsyncRead(self.handle)
        if (self.config.ch1_enabled) and (self.config.ch2_enabled):
            ch1_pts=(np.array(self.avg_data[:self.config.samplesPerRecord])-128.)*(self.config.ch1_range/128.)
            ch2_pts=(np.array(self.avg_data[self.config.samplesPerRecord:])-128.)*(self.config.ch2_range/128.)
        elif (self.config.ch1_enabled):
            ch1_pts=(np.array(self.avg_data)-128.)*(self.config.ch1_range/128.)
            ch2_pts=np.zeros(len(ch1_pts))
        else: return None,None
        tpts=np.arange(self.config.samplesPerRecord)/float(self.config.sample_rate*1e3)
        if excise is not None:
            return tpts[excise[0]:excise[1]],ch1_pts[excise[0]:excise[1]],ch2_pts[excise[0]:excise[1]]
        else:
            return tpts,ch1_pts,ch2_pts

if __name__ == "__main__":
    ac=AlazarConfig1(fedit(AlazarConfig1._form_fields_))

    card=Alazar(ac)    
    card.configure()
    card.acquire_data()

    print "Buffer bytes: ", card.config.bytesPerBuffer
    print "Buffer length: ",card.arrs[0].__len__()
    ion()
    figure(1)
    plot(card.arrs[0])
    figure(2)
    plot(card.arrs[0][:2048])
    figure(3)
    plot(card.arrs[-1][:2048])
    show()
