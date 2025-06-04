def check_cooldown(attack_in_progress, last_attack_time, cooldown_seconds):
    import time
    if attack_in_progress:
        return False, "⏳ Ya hay un ataque en curso, espera a que termine antes de iniciar otro"
    if time.time() - last_attack_time < cooldown_seconds:
        return False, f"😴 Debes esperar {int(cooldown_seconds - (time.time() - last_attack_time))} segundos antes de lanzar otro ataque"
    return True, ""
