#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Mono FM Radio
# Description: WFM receiver (mono only)
# GNU Radio version: 3.7.13.4
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import time
import wx


class radhachakrishna(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Mono FM Radio")

        ##################################################
        # Variables
        ##################################################
        self.usrp_freq = usrp_freq = 2414e6
        self.samp_rate = samp_rate = 500e3
        self.rx_freq = rx_freq = usrp_freq
        self.rf_gain = rf_gain = 30
        self.filter_taps = filter_taps = firdes.low_pass(1, samp_rate, 250000, 20000, firdes.WIN_HAMMING, 6.76)
        self.af_gain = af_gain = 0.5

        ##################################################
        # Blocks
        ##################################################
        _usrp_freq_sizer = wx.BoxSizer(wx.VERTICAL)
        self._usrp_freq_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_usrp_freq_sizer,
        	value=self.usrp_freq,
        	callback=self.set_usrp_freq,
        	label='USRP frequency',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._usrp_freq_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_usrp_freq_sizer,
        	value=self.usrp_freq,
        	callback=self.set_usrp_freq,
        	minimum=2000e6,
        	maximum=2500e6,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_usrp_freq_sizer)
        self._rx_freq_static_text = forms.static_text(
        	parent=self.GetWin(),
        	value=self.rx_freq,
        	callback=self.set_rx_freq,
        	label='Receive',
        	converter=forms.float_converter(),
        )
        self.Add(self._rx_freq_static_text)
        _rf_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._rf_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_rf_gain_sizer,
        	value=self.rf_gain,
        	callback=self.set_rf_gain,
        	label='RF',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._rf_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_rf_gain_sizer,
        	value=self.rf_gain,
        	callback=self.set_rf_gain,
        	minimum=0,
        	maximum=100,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_rf_gain_sizer)
        self.nbook = self.nbook = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.nbook.AddPage(grc_wxgui.Panel(self.nbook), "Receiver")
        self.nbook.AddPage(grc_wxgui.Panel(self.nbook), "Audio")
        self.Add(self.nbook)
        _af_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._af_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_af_gain_sizer,
        	value=self.af_gain,
        	callback=self.set_af_gain,
        	label='AF',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._af_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_af_gain_sizer,
        	value=self.af_gain,
        	callback=self.set_af_gain,
        	minimum=0,
        	maximum=10,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_af_gain_sizer)
        self.xlating_fir_filter = filter.freq_xlating_fir_filter_ccc(1, (filter_taps), 98.1, samp_rate)
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
        	self.nbook.GetPage(1).GetWin(),
        	title='Scope Plot',
        	sample_rate=samp_rate,
        	v_scale=0,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label='Counts',
        	size=(400,400),
        )
        self.nbook.GetPage(1).Add(self.wxgui_scopesink2_0.win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(('', '')),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(usrp_freq, 0)
        self.uhd_usrp_source_0.set_gain(rf_gain, 0)
        self.uhd_usrp_source_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_source_0.set_auto_dc_offset(False, 0)
        self.uhd_usrp_source_0.set_auto_iq_balance(False, 0)
        self.rr_stereo_right = filter.rational_resampler_fff(
                interpolation=48,
                decimation=50,
                taps=None,
                fractional_bw=None,
        )
        self.fftsink_rf = fftsink2.fft_sink_c(
        	self.nbook.GetPage(0).GetWin(),
        	baseband_freq=rx_freq,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=-30,
        	ref_scale=1.0,
        	sample_rate=samp_rate/2,
        	fft_size=512,
        	fft_rate=10,
        	average=True,
        	avg_alpha=0.5,
        	title='Baseband',
        	peak_hold=False,
        	size=(400,400),
        )
        self.nbook.GetPage(0).Add(self.fftsink_rf.win)
        self.audio_sink = audio.sink(48000, '', True)
        self.analog_wfm_rcv = analog.wfm_rcv(
        	quad_rate=samp_rate,
        	audio_decimation=10,
        )
        self.af_gain_stereo_left = blocks.multiply_const_vff((af_gain, ))



        ##################################################
        # Connections
        ##################################################
        self.connect((self.af_gain_stereo_left, 0), (self.audio_sink, 0))
        self.connect((self.af_gain_stereo_left, 0), (self.wxgui_scopesink2_0, 0))
        self.connect((self.analog_wfm_rcv, 0), (self.rr_stereo_right, 0))
        self.connect((self.rr_stereo_right, 0), (self.af_gain_stereo_left, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.xlating_fir_filter, 0))
        self.connect((self.xlating_fir_filter, 0), (self.analog_wfm_rcv, 0))
        self.connect((self.xlating_fir_filter, 0), (self.fftsink_rf, 0))

    def get_usrp_freq(self):
        return self.usrp_freq

    def set_usrp_freq(self, usrp_freq):
        self.usrp_freq = usrp_freq
        self._usrp_freq_slider.set_value(self.usrp_freq)
        self._usrp_freq_text_box.set_value(self.usrp_freq)
        self.set_rx_freq(self.usrp_freq)
        self.uhd_usrp_source_0.set_center_freq(self.usrp_freq, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_filter_taps(firdes.low_pass(1, self.samp_rate, 250000, 20000, firdes.WIN_HAMMING, 6.76))
        self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.fftsink_rf.set_sample_rate(self.samp_rate/2)

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        self._rx_freq_static_text.set_value(self.rx_freq)
        self.fftsink_rf.set_baseband_freq(self.rx_freq)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self._rf_gain_slider.set_value(self.rf_gain)
        self._rf_gain_text_box.set_value(self.rf_gain)
        self.uhd_usrp_source_0.set_gain(self.rf_gain, 0)


    def get_filter_taps(self):
        return self.filter_taps

    def set_filter_taps(self, filter_taps):
        self.filter_taps = filter_taps
        self.xlating_fir_filter.set_taps((self.filter_taps))

    def get_af_gain(self):
        return self.af_gain

    def set_af_gain(self, af_gain):
        self.af_gain = af_gain
        self._af_gain_slider.set_value(self.af_gain)
        self._af_gain_text_box.set_value(self.af_gain)
        self.af_gain_stereo_left.set_k((self.af_gain, ))


def main(top_block_cls=radhachakrishna, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
