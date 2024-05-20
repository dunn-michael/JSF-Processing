import os

# Goes through your directory to find files
# directory = 'Sidescans/'
directory = 'JSF-Processing/Sidescans/'
for filename in os.listdir(directory):
    if filename.endswith('.JSF'):
        with open(os.path.join(directory, filename), 'rb') as f:
            length = f.read()
            for i in range(len(length)):

                # This is here for testing to speed up tests
                # f.seek(0 + i * data_struct.size)

                # This will be the normal one
                f.seek(i)

