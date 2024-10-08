# Balloon Game with Mediapipe

This project is a simple and fun balloon-popping game built using [Mediapipe](https://mediapipe.dev/), an open-source framework for building perception pipelines. The game tracks hand movements using a webcam and lets players pop balloons by interacting with the screen through hand gestures.

## Features

- **Hand Gesture Tracking**: Uses Mediapipe to track hand gestures via the webcam.
- **Real-time Interaction**: Pop balloons on the screen by moving your hand.
- **Visual Effects**: Colorful balloons with popping animations when they are hit by hand gestures.
  
## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You will need the following installed on your system:

- [Python 3.8+](https://www.python.org/downloads/)
- [Mediapipe Library](https://google.github.io/mediapipe/getting_started/python.html)
- OpenCV

Install the necessary libraries using pip:

```bash
pip install mediapipe opencv-python
```

### Installation

1. Clone the repository:

```bash
git clone https://github.com/shivah12/Balloon_Game_Mediapipe.git
cd Balloon_Game_Mediapipe
```

2. Run the game script:

```bash
python balloon_game.py
```

Make sure your webcam is connected. The game will automatically start tracking your hand gestures and show balloons on the screen.

## How to Play

- The game will display balloons on the screen.
- Move your hand in front of the webcam to pop the balloons.
- The score will be updated each time you successfully pop a balloon.

## Built With

- [Mediapipe](https://mediapipe.dev/) - Hand tracking and gesture recognition.
- [OpenCV](https://opencv.org/) - Real-time computer vision for rendering game visuals.

## Contributing

Feel free to fork this repository, make changes, and submit a pull request. Any contributions to improve the game or add new features are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Mediapipe team for their awesome hand-tracking library.
- Inspired by various gesture-controlled games.
