import os
from math import pi, cos, sin, sqrt

def deltaPhi(phi1, phi2):
    dphi = phi2-phi1
    if  dphi > pi:
        dphi -= 2.0*pi
    if dphi <= -pi:
        dphi += 2.0*pi
    return abs(dphi)

def deltaR2(l1, l2):
    return deltaPhi(l1['phi'], l2['phi'])**2 + (l1['eta'] - l2['eta'])**2

def getVarValue(c, var, n=-1):
    att = getattr(c, var)
    if n>=0:
#    print "getVarValue %s %i"%(var,n)
        if n<att.__len__():
            return att[n]
        else:
            return float('nan')
    return att

def getObjDict(c, prefix, variables, i):
    res={var: getVarValue(c, prefix+var, i) for var in variables}
    res['index']=i
    return res

def getSubDir(dataset, path):
    import re
    m=re.match("\/(.*)\/(.*)\/(.*)",dataset)
    if not m :
        print "NO GOOD DATASET"
        return
    if os.environ['USER'] in ['tomc']: 
      d=re.match("(.*)/cmgTuples/(.*)",path)
      return m.group(1)+"/"+m.group(2)+'_'+d.group(2)
    else :                             
      return m.group(1)+"_"+m.group(2)

def fromHeppySample(sample, data_path, module = None, maxN = None):
    ''' Load CMG tuple from local directory
    '''

    from RootTools.core.Sample import Sample

    import importlib
    if module is not None:
        module_ = module
    elif "Run2016" in sample:
        module_ = 'CMGTools.RootTools.samples.samples_13TeV_DATA2016'
    elif "T2tt" in sample:
        module_ = 'CMGTools.RootTools.samples.samples_13TeV_signals'
    else: 
        module_ = 'CMGTools.RootTools.samples.samples_13TeV_RunIISpring16MiniAODv2'

    try:
        heppy_sample = getattr(importlib.import_module( module_ ), sample)
    except:
        raise ValueError( "Could not load sample '%s' from %s "%( sample, module_ ) )

    # helpers
    subDir = getSubDir(heppy_sample.dataset, data_path)
    if not subDir:
        raise ValueError( "Not a good dataset name: '%s'"%heppy_sample.dataset )

    path = os.path.join( data_path, subDir )
    sample = Sample.fromCMGOutput(
        heppy_sample.name, 
        path, 
        treeFilename = 'tree.root', 
        treeName = 'tree', isData = heppy_sample.isData, maxN = maxN)

    sample.heppy = heppy_sample
    return sample
