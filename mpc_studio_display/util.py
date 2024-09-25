def clamp(val, minv, maxv):
    return max(minv, min(val, maxv))

def message_length(message):
        length = len(message)
        return (
        clamp(length // 128, 0, 127), length % 128)

def msblsb(number):
    return (clamp(number // 128, 0, 127), number % 128)