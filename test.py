def main():
  def input0():
    return input("")
  def f(a):
    if a=="1":
      return print("Hello, world!")
    elif a=="0":
      return print("hello world")
    else:
      return 0
  while True:
    a=input0()
    f(a)
  return 0
main()
