# Signal_Processing
Here I put some of my (janky) hand written Python scripts used for SP.

The purpose of this repository is to keep at hand some functions that I have developed personally in the context of the laboratoy courses in my Master degree. Some of these routines already exist in Python, therefore they are just a rough rewriting of more sophisticated and optimized code, while some of them are specifically designed for my lab experiences. 

I have to say, I do not put __ALL__ my code here, but just what would be cumbersome and tedious to rewrite in the possible future. As mentioned in my [README.md document](https://github.com/Grafton17), the purpose of my repositories is just that of note keeping. I do not intend to be extremely systematic and tidy.

# Scope of laboratory courses
A (very short and not exhaustive) list of the objectives of the lab courses:
- PLASMA PHYSICS I: investigate the formation of travelling linear waves in a simulated plasma system;
- PLASMA PHYSICS I: analyze the turbulent plasma state inside the [Thorello device](https://fusenet.eu/node/517).

# Summary

In the [Libraries.py](Libraries.py) file I list all the modules used throughout the entire repository. Just add the content of this file at the beginning of your executable!

- [Bi-spectral analysis](Bi-coherence): bi-spetrum, bi-coherence and summed bi-coherence, useful tools in the search of wave-wave coupling phenomena.
- The [Conditional Sampling](Conditional-Sampling) technique, in my case used for the search of coherent structures inside a Simply Magnetized Plasma (SMP).
- Statistical evaluation of the [Dispersion Relation k(f)](Dispersion-Relation): in case the estimated linear coherence between two signals is way less than one, this approach permits to establish whether a travelling linear wave between two spots exists or not.
