# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased] - yyyy-mm-dd

### Added
 - MINOR if the velocity for the first direction is too high (>= 400 and v0 > v1 * 1.5), we will increase the velocity for the second direction as this will look like a float for the first direction but will be a Acc for the second making us gain about 22k points on the example B without changing anything to the others.
 - MINOR added the --display option, this will show the travel made by the santa on the map. It also save the representation every movement and create a GIF at the end in the output file.

## [0.1.0] - 2022-12-13

### Added
 - MINOR tests have been added for testing the differents classes
 - MINOR output is now created if not existant

### Changed

### Fixed
 - MINOR .gitlab-ci.yml file was not working properly

## [0.2.0] - 2022-12-14

### Changed
 - MINOR improve the time to generate the output file by filtering then looping over the gifts.  
    We did this by intersecting the range of the value to look into and the key of the dictionary containing every gift.

### Fixed
 - MINOR we now take into account that the range can be zero.  
    This was resolved by making the range 1 if no gift is found in the range.

## [0.3.0] - 2022-12-14

### Added 
 - MINOR Exception handling when the time is up inside the resolve loop in case we had an error with the time during our parcours to make it possible to have an output even if it's not perfect.   
    This will need to be fixed in the future.

### Changed
 - MAJOR the implementation of the class Acceleration has been changed to be more efficient:  
    we now accelerate everytime we can, this makes it so we go WAY faster when gifts (and start) are far away. 
    This implementation does not take into account the fact that we could accelerate diagonaly so it's still not performing as best but it's a good start.

## [0.4.0] - 2022-12-20

### Changed
 - MAJOR the implementation of Acceleration is more efficient:
    we now dont float while doing the acceleration for the shorter movement of the 2 direction this allows us to go faster and be quicker. 
 - MINOR the generation part of our solving is better as the Organiser only does 2 loops instead of 5 or 6 previously making it faster but also easier to maintain.