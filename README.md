# HEYY - some simple utilities

## Usage

```python
import heyy

# Temporarily change the working directory
# to complete some IO operation (e.g. save data to files)
@heyy.with_folder('my_folder')
def some_io_operation():
    pass

# convert dict to object
import requests
res = requests.get('<url>')
data = res.json()
dict_obj = heyy.json2obj(data)

# reflect attrs and values of an object
obj = dict_obj
heyy.reflect(obj, skip_callable=True)  # default False
```