from config import DATABASE_URI
from sqlalchemy import create_engine
from models import Base
import numpy as np
from psycopg2.extensions import register_adapter, AsIs

engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)



def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)

def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)

def addapt_numpy_float32(numpy_float32):
    return AsIs(numpy_float32)

def addapt_numpy_int32(numpy_int32):
    return AsIs(numpy_int32)

def addapt_numpy_array(numpy_array):
    return AsIs(tuple(numpy_array))

register_adapter(np.float64, AsIs)
register_adapter(np.int64, AsIs)
register_adapter(np.float32, AsIs)
register_adapter(np.int32, AsIs)
register_adapter(np.ndarray, AsIs)