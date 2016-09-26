from heppy.framework.analyzer import Analyzer
from heppy.papas.pdt import particle_data
from heppy.papas.pfobjects import Particle #so that Gun can be used in papas (needs uniqueid)
from ROOT import TVector3
#from heppy.particles.tlv.particle import Particle 

import math
import heppy.statistics.rrandom as random

from ROOT import TLorentzVector

def particle(pdgid, thetamin, thetamax, ptmin, ptmax, flat_pt=False):
    mass, charge = particle_data[pdgid]
    theta = random.uniform(thetamin, thetamax)
    phi = random.uniform(-math.pi, math.pi)
    energy = random.uniform(ptmin, ptmax)
    costheta = math.cos(math.pi/2. - theta)
    sintheta = math.sin(math.pi/2. - theta)
    tantheta = sintheta / costheta
    cosphi = math.cos(phi)
    sinphi = math.sin(phi)    
    vertex = TVector3(0,0,0)
    if flat_pt:
        pt = energy
        momentum = pt / sintheta
        energy = math.sqrt(momentum**2 + mass**2)
    else:
        momentum = math.sqrt(energy**2 - mass**2)
    tlv = TLorentzVector(momentum*sintheta*cosphi,
                         momentum*sintheta*sinphi,
                         momentum*costheta,
                         energy)
    #return Particle(pdgid, vertex, charge, tlv) #tlv
    return Particle(tlv, vertex, charge, pdgid) #pfobjectrs
    

class Gun(Analyzer):
    
    def process(self, event):
        event.gen_particles = [particle(self.cfg_ana.pdgid, 
                                        self.cfg_ana.thetamin, 
                                        self.cfg_ana.thetamax,
                                        self.cfg_ana.ptmin, 
                                        self.cfg_ana.ptmax,
                                        flat_pt=self.cfg_ana.flat_pt)]
        event.gen_particles_stable = event.gen_particles
