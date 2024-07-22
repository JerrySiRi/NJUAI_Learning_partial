phase_35 = 'phase_3.5/audio/sfx/'
phase_4 = 'phase_4/audio/sfx/'
phase_5 = 'phase_5/audio/sfx/'

sounds = {
  'pie_throw' : phase_35 + 'AA_pie_throw_only',
  'tart_coll' : phase_35 + 'AA_tart_only',
  'pie_coll' : phase_4 + 'AA_wholepie_only',
  'propeller' : phase_4 + 'TB_propeller',
  'propeller_in' : phase_5 + 'ENC_propeller_in',
  'cog_laugh' : phase_35 + 'Cog_Death',
  'cog_explode' : phase_35 + 'ENC_cogfall_apart',
  'skelecog_grunt' : phase_5 + 'Skel_COG_VO_grunt',
  'skelecog_murmur' : phase_5 + 'Skel_COG_VO_murmur',
  'skelecog_question' : phase_5 + 'Skel_COG_VO_question',
  'skelecog_statement' : phase_5 + 'Skel_COG_VO_statement',
  'victory_dance' : phase_35 + 'ENC_Win',
  'door_open' : phase_35 + 'Door_Open_1',
  'door_close' : phase_35 + 'Door_Close_1',
  'toon_walk' : phase_35 + 'AV_footstep_walkloop',
  'toon_run' : phase_35 + 'AV_footstep_runloop',
  'make_a_toon' : 'phase_3/audio/bgm/create_a_toon',
  'drop_pickup' : 'phase_5.5/audio/sfx/mailbox_alert',
  'bgm_doom' : 'bgm/Doomsday Theme',
  'bgm_ceo' : 'bgm/BossBot_CEO_v2',
  'bgm_bigboss' : 'bgm/The Big Boss',
  'bgm_install' : 'bgm/Installer Theme',
  'bgm_hall' : 'bgm/Hall of Fame',
  'bgm_orchestra' : 'bgm/Installer Orchestrated.mp3',
  'bgm_bldg' : 'bgm/encntr_suit_winning_indoor',
  'cannon_fire' : phase_4 + 'MG_cannon_fire_alt',
  'cannon_adjust' : phase_4 + 'MG_cannon_adjust',
  'cannon_whizz' : phase_4 + 'MG_cannon_whizz',
  'toonhall_warning' : 'sfx/CHQ_GOON_tractor_beam_alarmed',
  'power_tie_throw' : phase_5 + 'SA_powertie_throw',
  'power_tie_impact' : phase_5 + 'SA_powertie_impact'
}

def getSound(soundName):
    if('mp3' not in sounds[soundName]):
        sound = loader.loadSfx(sounds[soundName] + '.ogg')
    else:
        sound = loader.loadSfx(sounds[soundName])
    return sound