
Introduction
----------------------------

This is a modified version of v0.7.7 of the monte CC project: http://www.randelshofer.ch/monte/

The source can be downloaded here: http://www.randelshofer.ch/monte/files/MonteMedia-0.7.7src-cc.zip



License Terms
----------------------------
(Copied and pasted from http://www.randelshofer.ch/monte )

Use of the Monte Media Library is free for all uses (non-commercial, commercial and educational) 
under the terms of Creative Commons Attribution 3.0 (CC BY 3.0).

Attribution: Please leave an attribution to me in the source files.


Building
-------------------------------

1. First build the java code:

```
cd resources/MonteMediaCC
ant
```

2. Now Create the jar package:

```
cd resources/MonteMediaCC/build/classes
jar cfm ScreenRecord.jar ../../screen_record_manifest.mf ScreenRecorder.class org
mv ScreenRecord.jar ../../..
```

Running
-------------------------------

You need to pass a quicktime parameter to the jar:

```
java -jar ScreenRecord.jar /tmp/my_screengrab.mov
```
