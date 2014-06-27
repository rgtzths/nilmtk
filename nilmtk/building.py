from __future__ import print_function, division
from collections import namedtuple
from .metergroup import MeterGroup
from .datastore import join_key

BuildingID = namedtuple('BuildingID', ['instance', 'dataset'])

class Building(object):   
    """
    Attributes
    ----------
    elec : MeterGroup

    metadata : dict
        Metadata just about this building (e.g. geo location etc).
        See http://nilm-metadata.readthedocs.org/en/latest/dataset_metadata.html#building
        Has these additional keys: 
        dataset : string
    """
    def __init__(self):
        self.elec = MeterGroup()
        self.metadata = {}
    
    def load(self, store, key):
        self.metadata = store.load_metadata(key)
        elec_meters = self.metadata.pop('elec_meters', {})
        appliances = self.metadata.pop('appliances', [])
        self.elec.load(store, elec_meters, appliances, self.identifier)
                
    def save(self, destination, key):
        destination.write_metadata(key, self.metadata)
        self.elec.save(destination, join_key(key, 'elec'))

    @property
    def identifier(self):
        md = self.metadata
        return BuildingID(instance=md.get('instance'), 
                          dataset=md.get('dataset'))