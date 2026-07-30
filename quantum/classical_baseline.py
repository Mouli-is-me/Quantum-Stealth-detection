def classical_sensor_fusion(scores, threshold=0.6):
    """
    Classical weighted sensor fusion baseline.
    """

    radar = scores["Radar"]
    infrared = scores["Infrared"]
    acoustic = scores["Acoustic"]

    fusion_score = (
        radar * 0.40 +
        infrared * 0.30 +
        acoustic * 0.30
    )

    detected = fusion_score >= threshold

    return {
        "fusion_score": round(fusion_score, 3),
        "detected": detected,
        "method": "Classical Weighted Fusion"
    }

