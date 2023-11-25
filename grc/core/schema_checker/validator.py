# Copyright 2016 Free Software Foundation, Inc.
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-2.0-or-later
#


from .utils import Message, Spec
import re


class ValidationError(Exception):
    pass


class Validator(object):
    def __call__(self, data):
        self.validate(data)


class Bool(Validator):
    def validate(self, data):
        assert isinstance(data, bool)


class Int(Validator):
    def validate(self, data):
        assert isinstance(data, int)


class Float(Validator):
    def validate(self, data):
        assert isinstance(data, float)


class Str(Validator):
    def __init__(self, regex: str=None):
        self._regex = regex
        if regex is not None:
            if not regex.endswith(r'$'):
                regex += r'$'
            self._fullmatch = re.compile(regex).match

    def validate(self, data):
        assert isinstance(self, str)
        if self._regex is None:
            return
        if self._fullmatch(data) is None:
            raise ValidationError(
                f"'{data}' does not match r'{self._regex}'"
            )


class Option(Validator):
    def __init__(self, validator: Validator=None):
        assert validator is None or isinstance(validator, Validator)
        self._inner = validator
    
    def validate(self, data):
        if data is not None:
            self._inner.validate(data)


class Dict(Validator, dict):
    def __init__(self, map, **kwargs):
        dict.__init__(self, map, **kwargs)

        for v in self.values():
            assert isinstance(v, Validator)
    
    def validate(self, data):
        assert isinstance(data, dict)

        errors = []
        for k, v in self.entries():
            try:
                v.validate(data[k])
            except KeyError:
                if not isinstance(v, Option):
                    errors.append(ValidationError(
                        f"Required key '{k}' not found in {data}"
                    ))
            except ValidationError as e:
                errors.append(e)
        
        if len(errors) > 0:
            raise ValidationError(errors)


class Mapping(Validator):
    def __init__(self, key_validator: Validator=Str(), 
                 value_validator: Validator=None):
        assert isinstance(key_validator, Validator)
        assert isinstance(value_validator, (Validator, type(None)))
        self._key_validator = key_validator
        self._value_validator = value_validator

    def validate(self, data):
        assert isinstance(data, dict)

        errors = []
        for k, v in data:
            try:
                self._key_validator.validate(k)
                self._value_validator.validate(v)
            except ValidationError as e:
                errors.append(e)
        
        if len(errors) > 0:
            raise ValidationError(errors)


class FixedSeq(Validator, list):
    def __init__(self, iterable):
        list.__init__(iterable)

        for v in self:
            assert isinstance(v, Validator)

    def validate(self, data):
        assert isinstance(data, list)

        errors = []
        for v, d in zip(self, data):
            try:
                v.validate(d)
            except ValidationError as e:
                errors.append(e)
        
        if len(errors) > 0:
            raise ValidationError(errors)


class Seq(Validator):
    def __init__(self, item_validator: Validator=None, len_min=0, len_max=float('inf')):
        assert item_validator is None or isinstance(item_validator, Validator)
        self._item_validator = item_validator
        self._len_min = len_min
        self._len_max = len_max

    def validate(self, data):
        assert isinstance(data, list)
        assert len(data) >= self._len_min
        assert len(data) <= self._len_max
        if self._item_validator is None:
            return

        errors = []
        for d in data:
            try:
                self._item_validator.validate(d)
            except ValidationError as e:
                errors.append(e)

        if len(errors) > 0:
            raise ValidationError(errors)


class OrValidator(Validator, list):
    def __init__(self, *validators):
        assert len(validators) > 1

        self._validators = []
        for v in validators:
            assert isinstance(v, Validator)
            if isinstance(v, OrValidator):
                self._validators.extend(v._validators)
            else:
                self._validators.append(v)
        
    def validate(self, data):
        for v in self._validators:
            try:
                v.validate(data)
                return
            except ValidationError:
                pass
        
        raise ValidationError('No matching validator '
                              f'for {data} in {self._validators}')



class Validator_old(object):

    def __init__(self, scheme=None):
        self._path = []
        self.scheme = scheme
        self.messages = []
        self.passed = False

    def run(self, data):
        if not self.scheme:
            return True
        self._reset()
        self._path.append('block')
        self._check(data, self.scheme)
        self._path.pop()
        return self.passed

    def _reset(self):
        del self.messages[:]
        del self._path[:]
        self.passed = True

    def _check(self, data, scheme):
        if not data or not isinstance(data, dict):
            self._error('Empty data or not a dict')
            return
        if isinstance(scheme, dict):
            self._check_dict(data, scheme)
        else:
            self._check_var_key_dict(data, *scheme)

    def _check_var_key_dict(self, data, key_type, value_scheme):
        for key, value in data.items():
            if not isinstance(key, key_type):
                self._error('Key type {!r} for {!r} not in valid types'.format(
                    type(value).__name__, key))
            if isinstance(value_scheme, Spec):
                self._check_dict(value, value_scheme)
            elif not isinstance(value, value_scheme):
                self._error('Value type {!r} for {!r} not in valid types'.format(
                    type(value).__name__, key))

    def _check_dict(self, data, scheme):
        for key, (types_, required, item_scheme) in scheme.items():
            try:
                value = data[key]
            except KeyError:
                if required:
                    self._error('Missing required entry {!r}'.format(key))
                continue

            self._check_value(value, types_, item_scheme, label=key)

        for key in set(data).difference(scheme):
            self._warn('Ignoring extra key {!r}'.format(key))

    def _check_list(self, data, scheme, label):
        for i, item in enumerate(data):
            self._path.append('{}[{}]'.format(label, i))
            self._check(item, scheme)
            self._path.pop()

    def _check_value(self, value, types_, item_scheme, label):
        if not isinstance(value, types_):
            self._error('Value type {!r} for {!r} not in valid types'.format(
                type(value).__name__, label))
        if item_scheme:
            if isinstance(value, list):
                self._check_list(value, item_scheme, label)
            elif isinstance(value, dict):
                self._check(value, item_scheme)

    def _error(self, msg):
        self.messages.append(Message('.'.join(self._path), 'error', msg))
        self.passed = False

    def _warn(self, msg):
        self.messages.append(Message('.'.join(self._path), 'warn', msg))
