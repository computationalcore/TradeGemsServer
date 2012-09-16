"""Utility classes and methods for use with json and appengine.

Provides both a specialized json encoder, GqlEncoder, designed to simplify
encoding directly from GQL results to JSON. A helper function, encode, is also
provided to further simplify usage.

  GqlEncoder: Adds support for GQL results and properties to json.
  encode(input): Direct method to encode GQL objects as JSON.
"""

import datetime
import json
import time

from google.appengine.api import users
from google.appengine.ext import db

from model import User, user_key, Player


class GqlEncoder(json.JSONEncoder):

    """Extends JSONEncoder to add support for GQL results and properties.

    Adds support to json JSONEncoders for GQL results and properties by
    overriding JSONEncoder's default method.
    """

    # TODO Improve coverage for all of App Engine's Property types.

    def default(self, obj):

        """Tests the input object, obj, to encode as JSON."""

        if hasattr(obj, '__json__'):
            return getattr(obj, '__json__')()

        if isinstance(obj, db.GqlQuery):
            return list(obj)

        elif isinstance(obj, db.Model):
            properties = obj.properties().items()
            output = {}

            if isinstance(obj, Player):
                #only valid for Player obj
                user = obj.parent()
                output['nickname'] = user.nickname
            for field, value in properties:
                #Convert Datastore time and convert to timestamp
                obj_field = getattr(obj, field)
                if isinstance(obj_field, datetime.datetime):
                    output[field] = time.mktime(obj_field.timetuple())
                else:
                    output[field] = getattr(obj, field)
            return output

        return json.JSONEncoder.default(self, obj)


def encode(input):
    """Encode an input GQL object as JSON

    Args:
      input: A GQL object or DB property.

    Returns:
      A JSON string based on the input object.

    Raises:
      TypeError: Typically occurs when an input object contains an unsupported
        type.
    """
    return GqlEncoder().encode(input)