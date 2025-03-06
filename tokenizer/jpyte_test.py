import jpype

jvmpath = r"C:\Program Files\Java\jdk-17.0.12\bin\server\jvm.dll"
jpype.startJVM(jvmpath)
print("JVM started successfully!")
jpype.shutdownJVM()