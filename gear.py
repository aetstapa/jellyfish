import numpy as np
import wave

# =====================
# 参数
# =====================
sample_rate = 44100
click_sound_duration = 2.0  # 滚轮咯哒声总时长
silence_duration = 1.0  # 前面静音

click_rate_min = 3
click_rate_max = 18
click_duration = 0.0012  # 单个 click 时长
volume = 1

# =====================
# 缓冲区
# =====================
total_samples = int(sample_rate * click_sound_duration)
audio = np.zeros(total_samples)

# =====================
# iPod 风格 click 波形
# =====================
click_len = int(click_duration * sample_rate)
t_click = np.linspace(0, click_duration, click_len, False)

# 白噪声 + 阻尼
noise = np.random.randn(click_len)
envelope = np.exp(-t_click * 6500)
filtered = noise - 0.6 * np.roll(noise, 1)
filtered[0] = 0
click_wave = filtered * envelope

# =====================
# 相位累加（对称速度包络）
# =====================
phase = 0.0
click_count = 0

for i in range(total_samples):
    t = i / sample_rate
    x = t / click_sound_duration  # 注意这里使用滚轮总时长 2 秒

    # 对称速度包络
    speed = 0.5 * (1 - np.cos(2 * np.pi * x))
    click_rate = click_rate_min + (click_rate_max - click_rate_min) * speed

    # 轻微随机化
    click_rate *= np.random.uniform(0.95, 1.05)

    phase += click_rate / sample_rate

    if phase >= 1.0:
        phase -= 1.0
        click_count += 1

        # 微弱重音，每 4 个 click 略强
        if click_count % 4 == 0:
            strength = np.random.uniform(0.85, 1.0)
        else:
            strength = np.random.uniform(0.7, 0.9)

        end = min(i + click_len, total_samples)
        audio[i:end] += strength * click_wave[: end - i]

# =====================
# 在前面加 1 秒静音
# =====================
silence_samples = int(silence_duration * sample_rate)
audio = np.concatenate((np.zeros(silence_samples), audio))

# =====================
# 归一化 & 写 WAV
# =====================
audio /= np.max(np.abs(audio))
audio = np.int16(audio * volume * 32767)

with wave.open("videos/gear.wav", "w") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(sample_rate)
    f.writeframes(audio.tobytes())

print("gear.wav 已生成")
