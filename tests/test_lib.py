import sys
import pytest
from dataclasses import asdict
from pytest import MonkeyPatch
from abc import ABC, abstractmethod
from typing import cast, NoReturn
from errlypy.api import ExceptionCallback
from errlypy.lib import ExceptionCallbackImpl, CreateExceptionCallbackMeta, FrameDetail
from errlypy.utils import has_contract_been_implemented, has_dict_contract_been_implemented


class UncaughtExceptionFromRepr(Exception):
  def __init__(self, *args: object) -> None:
    super().__init__(*args)


class ExceptionCallbackImplWithInvalidRepr(ExceptionCallbackImpl):
  def __repr__(self) -> NoReturn:
    raise UncaughtExceptionFromRepr('Uncaught error for __repr__')


def test_exception_callback_impl_contract_success():
  instance = ExceptionCallbackImpl.create({}, CreateExceptionCallbackMeta())
  result = has_contract_been_implemented(instance, ExceptionCallback)

  assert result == True


def test_exception_callback_impl_contract_fail():
  class IncorrectCallback(ABC):
    @abstractmethod
    def incorrect_method(self):
      pass

  instance = ExceptionCallbackImpl.create({}, CreateExceptionCallbackMeta())
  result = has_contract_been_implemented(instance, IncorrectCallback)

  assert result == False

def test_exception_callback_impl_result_success():
  mpatch = MonkeyPatch()
  callback = ExceptionCallbackImpl.create(
    {},
    CreateExceptionCallbackMeta()
  )
  mpatch.setattr(sys, 'excepthook', callback)

  try:
    raise ValueError('Test')
  except ValueError as err:
    result = sys.excepthook(type(err), err, err.__traceback__)

  assert isinstance(result, dict)
  assert isinstance(result['data'], list)
  assert len(result['data']) > 0
  assert isinstance(result['data'][0], FrameDetail)


def test_exception_callback_impl_result_frame_detail_contract_success():
  mpatch = MonkeyPatch()
  callback = ExceptionCallbackImpl.create(
    {},
    CreateExceptionCallbackMeta()
  )
  mpatch.setattr(sys, 'excepthook', callback)

  try:
    raise ValueError('Test')
  except ValueError as err:
    result = sys.excepthook(type(err), err, err.__traceback__)

  frame_detail = result['data'][0]
  assert has_dict_contract_been_implemented(asdict(frame_detail), FrameDetail)


def test_exception_callback_impl_result_frame_detail_body_success():
  mpatch = MonkeyPatch()
  callback = ExceptionCallbackImpl.create(
    {},
    CreateExceptionCallbackMeta()
  )
  mpatch.setattr(sys, 'excepthook', callback)

  try:
    raise ValueError('Test')
  except ValueError as err:
    result = sys.excepthook(type(err), err, err.__traceback__)

  frame_detail = cast(FrameDetail, result['data'][0])
  assert frame_detail.function == 'test_exception_callback_impl_result_frame_detail_body_success'
  assert frame_detail.line == "raise ValueError('Test')"
  assert frame_detail.filename.endswith('test_lib.py') is True
  assert 'pytest.monkeypatch.MonkeyPatch object at' in frame_detail.locals['mpatch']
  assert 'errlypy.lib.ExceptionCallbackImpl object at' in frame_detail.locals['callback']


def test_exception_callback_impl_with_invalid_repr_result_frame_detail_body_success():
  mpatch = MonkeyPatch()
  callback = ExceptionCallbackImplWithInvalidRepr.create(
    {},
    CreateExceptionCallbackMeta()
  )
  mpatch.setattr(sys, 'excepthook', callback)

  try:
    raise ValueError('Test')
  except ValueError as err:
    with pytest.raises(UncaughtExceptionFromRepr):
      result = sys.excepthook(type(err), err, err.__traceback__)
