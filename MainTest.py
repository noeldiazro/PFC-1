#!/usr/bin/python
# -*- coding: utf-8 -*-

from classes import Simulator

s=Simulator.Simulator(500)
s.setFileInput("../../../Muestras csv/termod-amortiguado.csv")
s.start()