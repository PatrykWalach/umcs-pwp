import typing
import functools


P = typing.ParamSpec('P')

def convert_to(unit: typing.Literal["celcjusz", "fahrenheit"])->typing.Callable[[typing.Callable[P, float]],typing.Callable[P, float]]:
    if unit == "celcjusz":
      def converter (x: float)->float: return x - 273.15
    else:
      def converter (x: float)->float: return  x*1.8 - 459.67

    def decorator(f: typing.Callable[P, float])->typing.Callable[P, float]:
        @functools.wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs)->float:
            return converter(f(*args, **kwargs))

        return wrapper

    return decorator

if __name__ == "__main__":

  @convert_to('celcjusz')
  def get_temp()->int:
      return 301

  @convert_to('fahrenheit')
  def get_other_temp()->int:
      return 295

  print(get_temp())
  print(get_other_temp())
