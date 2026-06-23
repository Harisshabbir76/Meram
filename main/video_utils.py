"""
Video compression helpers for CMS hero/background uploads.

Requires ffmpeg/ffprobe to be installed on the server PATH.
"""

import os
import subprocess
import tempfile

from django.core.files.base import ContentFile


MAX_DURATION_SECONDS = 12
TARGET_SIZE_KB = 1500
MAX_WIDTH = 1280
FPS = 24
MIN_VIDEO_BITRATE_K = 180
MAX_VIDEO_BITRATE_K = 1200


class VideoCompressionError(Exception):
    pass


def _run(cmd):
    try:
        return subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            timeout=180,
        )
    except FileNotFoundError as exc:
        raise VideoCompressionError("ffmpeg is not installed on this server.") from exc
    except subprocess.TimeoutExpired as exc:
        raise VideoCompressionError("Video compression timed out.") from exc
    except subprocess.CalledProcessError as exc:
        msg = (exc.stderr or exc.stdout or "Video compression failed.").strip()
        raise VideoCompressionError(msg[-500:]) from exc


def _probe_duration(path):
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                path,
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return max(0.1, float(result.stdout.strip()))
    except FileNotFoundError as exc:
        raise VideoCompressionError("ffprobe is not installed on this server.") from exc
    except Exception:
        return MAX_DURATION_SECONDS


def _write_upload(uploaded_file, suffix):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    try:
        for chunk in uploaded_file.chunks():
            tmp.write(chunk)
        return tmp.name
    finally:
        tmp.close()


def _bitrate_for(duration):
    usable_duration = min(duration, MAX_DURATION_SECONDS)
    target_bits = TARGET_SIZE_KB * 1024 * 8
    bitrate_k = int((target_bits / usable_duration) / 1000)
    bitrate_k = int(bitrate_k * 0.88)
    return max(MIN_VIDEO_BITRATE_K, min(MAX_VIDEO_BITRATE_K, bitrate_k))


def compressed_hero_video(uploaded_file):
    """
    Return (filename, ContentFile) for a compressed, muted MP4 hero video.
    """
    original_name = uploaded_file.name or "hero-video"
    suffix = os.path.splitext(original_name)[1] or ".mp4"
    input_path = _write_upload(uploaded_file, suffix)
    output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    output_path = output_file.name
    output_file.close()

    try:
        duration = _probe_duration(input_path)
        bitrate_k = _bitrate_for(duration)
        vf = (
            "scale='min(%d,iw)':-2:force_original_aspect_ratio=decrease,"
            "fps=%d,format=yuv420p"
        ) % (MAX_WIDTH, FPS)

        _run(
            [
                "ffmpeg",
                "-y",
                "-i",
                input_path,
                "-t",
                str(MAX_DURATION_SECONDS),
                "-an",
                "-vf",
                vf,
                "-c:v",
                "libx264",
                "-preset",
                "medium",
                "-b:v",
                f"{bitrate_k}k",
                "-maxrate",
                f"{bitrate_k}k",
                "-bufsize",
                f"{bitrate_k * 2}k",
                "-movflags",
                "+faststart",
                output_path,
            ]
        )

        with open(output_path, "rb") as fp:
            data = fp.read()

        base = os.path.splitext(os.path.basename(original_name))[0] or "hero-video"
        return base + ".mp4", ContentFile(data)
    except VideoCompressionError:
        uploaded_file.seek(0)
        return original_name, ContentFile(uploaded_file.read())
    finally:
        for path in (input_path, output_path):
            try:
                os.remove(path)
            except OSError:
                pass
