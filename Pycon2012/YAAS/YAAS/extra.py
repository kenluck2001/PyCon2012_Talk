import hashlib
from django.db.models import ImageField
from django.forms import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
import random
import operator

class ContentTypeRestrictedFileField(ImageField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file size allowed for upload.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB 104857600
            250MB - 214958080
            500MB - 429916160
    """
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types")
        self.max_upload_size = kwargs.pop("max_upload_size")

        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):        
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)
        
        file = data.file
        try:
            content_type = file.content_type
            if content_type in self.content_types:
                if file._size > self.max_upload_size:
                    raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(self.max_upload_size), filesizeformat(file._size)))
            else:
                raise forms.ValidationError(_('Filetype not supported.'))
        except AttributeError:
            pass        
            
        return data


#This is needed to hash the user password.
def hashPassword(password):
    '''
        This is used to hash the password. The password is not saved in clear text.
    '''
    hashed_password = hashlib.sha1(password).hexdigest()
    return hashed_password


#This is needed for random number generation
def createRandom():
    '''
        This is used to generate random number
    '''
    strlenLimit, randomValue = 18, ""	
    val = random.randint(1, 100000000000000000)
    strLenght = len(str(val))
    if (strLenght < strlenLimit):
        randomValue = ('0' * abs(strLenght - strlenLimit)) + str(val)
    return randomValue

#This is used for session id generation
def generate_session_id():
    '''
        This is used to generate unique session id that can be used to conveniently identify unique user sessions.
    '''
    session_id = ''
    characters = 'ABCDEFGHIJKLMNOPQRQSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    session_id_length = 50
    for y in range(session_id_length):
        session_id += characters[random.randint(0, len(characters)-1)]
    return session_id




#get maximum key, value on dictionary
def maxValueBid(stats):
    #http://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
    key = max(stats.iteritems(), key=operator.itemgetter(1))[0]     #item id
    value = max(stats.iteritems(), key=operator.itemgetter(1))[1]   #bid count
    return key , value

#sort dictionary by value
def sortedItemDictionary(x):
    sorted_x = sorted(x.iteritems(), key=operator.itemgetter(1), reverse=True)[:10]
    return sorted_x


def uniq(alist):
    '''
        This is used to make a list element unique. This is implemented by enclosing a set in a list. This deletes duplicate
    '''
    set = {}
    return [set.setdefault(e,e) for e in alist if e not in set]


