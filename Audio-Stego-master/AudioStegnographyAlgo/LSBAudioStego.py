import os.path
import wave

from AudioStegnographyAlgo.AudioStegnographyAlgorithm import AudioStego


class LSBAudioStego(AudioStego):
    def saveToLocation(self, audioArray, location):
        # save to dir as output-lsb
        dir = os.path.dirname(location)
        self.newAudio = wave.open(dir + "/output-lsb.wav", 'wb')
        self.newAudio.setparams(self.audio.getparams())
        self.newAudio.writeframes(audioArray)
        self.newAudio.close()
        self.audio.close()
        return dir + "/output-lsb.wav"

    def encodeAudio(self, audioLocation, stringToEncode) -> str:
        # convert to array
        audioArray = self.convertToByteArray(audioLocation)
        # convert string to encode  into bit array
        stringToEncode = stringToEncode + int((len(audioArray) - (len(stringToEncode) * 8 * 8)) / 8) * '#'
        bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in stringToEncode])))
        # do lsb manipulation
        for i, bit in enumerate(bits):
            audioArray[i] = (audioArray[i] & 254) | bit
        encodedAudio = bytes(audioArray)
        return self.saveToLocation(encodedAudio, audioLocation)

    def decodeAudio(self, audioLocation) -> str:
        # reconstruct original message by converting to binary array
        audioArray = self.convertToByteArray(audioLocation)
        decodedArray = [audioArray[i] & 1 for i in range(len(audioArray))]
        self.audio.close()
        return \
            "".join(
                chr(int("".join(map(str, decodedArray[i:i + 8])), 2)) for i in range(0, len(decodedArray), 8)).split(
                "###")[0]

    def convertToByteArray(self, audioLocation):
        # convert to byte array
        self.audio = wave.open(audioLocation, mode="rb")
        return bytearray(list(self.audio.readframes(self.audio.getnframes())))
