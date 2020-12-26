MidiBaseStr = "/midi:*:*:*"

#Low Pass Filter vars
RLPF_Res = 0.5
RLPF_Cutoff = 100

+#Envelope vars
ENV_Attack = 0
ENV_Release = 1
ENV_Sustain = 0
ENV_Decay = 0
ENV_Attack_Level = 1
ENV_Decay_Level = 1
ENV_Curve = 1 #(1,3,6,7)

PITCH_ADJ = 0

MAX_NODES = 9
MidiSynthQueue = Queue.new #queued midi events for synth
MidiDrumQueue = Queue.new #queued midi events for drums

ns = [] #array to store note playing references
killList = []


128.times do |i|
  ns[i] = {node: nil, onStatus: 0}
end

InstrumentLookup = {0 => :piano, 1 => :pluck, 2 => :prophet, 3 => :blade, 4 => :dull_bell, 
                  5 => :pretty_bell, 6 => :hollow, 7 => :hoover, 8 => :tb303, 9 => :beep, 
                  10 => :sine, 11 => :saw, 12 => :pulse, 13 => :subpulse, 14 => :square, 
                  15 => :tri, 16 => :dsaw, 17 => :dpulse, 18 => :dtri, 19 => :fm, 
                  20 => :mod_fm, 21 => :mod_saw, 22 => :mod_dsaw, 23 => :mod_sine, 24 => :mod_beep, 
                  25 => :mod_tri, 26 => :mod_pulse, 27 => :supersaw, 28 => :dark_ambience, 29 => :growl, 
                  30 => :pnoise, 31 => :bnoise, 32 => :gnoise, 33 => :cnoise}

CurrentInstrument = 0

##########################################################################
#                      Read Midi Commands                                #
##########################################################################
define :getMidiCntrlObjFromMidiInput do |element, value, midiBase|
  #get full event for channel and operation values
  midiEvent = get_event(midiBase + "/*")
  channel_operation = midiEvent.to_s.split("\"")[1].split(":").last.split("/")

  if channel_operation[1] == "control_change"
    return {controlNum: element, value: value, operation: channel_operation[1], channel: channel_operation[0]}
  elsif channel_operation[1] == "program_change"
    return {value: value, operation: channel_operation[1], channel: channel_operation[0]} 
  end
  return {note: element, volume: value, operation: channel_operation[1], channel: channel_operation[0]}
end

in_thread(name: :read_midiNotes) do
  loop do
    use_real_time
    note, volume = sync MidiBaseStr + "/note_*"
    cmd = getMidiCntrlObjFromMidiInput note, volume, MidiBaseStr
  #drums are on channel 10
    if cmd[:channel] == "10"
      MidiDrumQueue << cmd
      cue :PlayDrumsSync
    else
      MidiSynthQueue << cmd
      #cue :PlaySynthSync
    end
  end
end

in_thread(name: :read_midiControl) do
  loop do
    use_real_time
    cntrlNum, value = sync MidiBaseStr + "/control_change"
    cmd = getMidiCntrlObjFromMidiInput cntrlNum, value, MidiBaseStr
    if cmd[:channel] == "16"
      setControlSettings cmd[:controlNum], cmd[:value]
    end
  end
end

in_thread(name: :read_midiProgramChange) do
  loop do
    use_real_time
    value = sync MidiBaseStr + "/program_change"
    #cmd = getMidiCntrlObjFromMidiInput 0, value, MidiBaseStr
    CurrentInstrument = value[0]
  end
end
##########################################################################
#                           Control Changes                              #
##########################################################################
define :scaleMidiAi do |rawVal, lowEu, highEu|
  val = (rawVal/127.0) * (highEu - lowEu) + lowEu
  return val
end

define :setControlSettings do |cntrlNum, cntrlValue|
  if cntrlNum == 53
    RLPF_Res = scaleMidiAi cntrlValue, 0, 0.9
  elsif cntrlNum == 39
    RLPF_Cutoff = scaleMidiAi cntrlValue, 50, 130
  elsif cntrlNum == 33
  #envelope
    ENV_Attack = scaleMidiAi cntrlValue, 0, 1
  elsif cntrlNum == 35
    ENV_Release = scaleMidiAi cntrlValue, 0, 2
  elsif cntrlNum == 34
    ENV_Decay = scaleMidiAi cntrlValue, 0, 1
  elsif cntrlNum == 36
    ENV_Attack_Level = scaleMidiAi cntrlValue, 0, 1
  elsif cntrlNum == 37
    ENV_Decay_Level = scaleMidiAi cntrlValue, 0, 1

  elsif cntrlNum == 32
    PITCH_ADJ = (scaleMidiAi cntrlValue, 0, 12) - 6
    if PITCH_ADJ < 0.1 && PITCH_ADJ > -0.1
      PITCH_ADJ = 0
    end
  elsif cntrlNum == 30
    set_volume! (scaleMidiAi cntrlValue, 0, 1)
  end
  #control FxNode, res: RLPF_Res, cutoff: RLPF_Cutoff
end

##########################################################################
#                            Play Synth                                  #
##########################################################################
#Midi controls thread
with_fx :rlpf do |rlpf|
with_fx :reverb do |reverb|
with_fx :echo do |echo|
with_fx :compressor do |compressor|
with_fx :whammy do |whammy|
with_fx :rhpf do |rhpf|
with_fx :distortion do |distortion|
with_fx :octaver do |octaver|
with_fx :flanger do |flanger|
with_fx :pitch_shift do |pitchShift|#PITCH_ADJ
  in_thread(name: :play_synth) do
    begin
      loop do
        use_real_time
        #sync :PlaySynthSync
        begin
          control pitchShift, pitch: PITCH_ADJ
          control rlpf, res: RLPF_Res, cutoff: RLPF_Cutoff
          while MidiSynthQueue.length > 0 do
            synth_doCommand MidiSynthQueue.deq
          end
        rescue
          print "synth failed"
        end
        sleep 0.05
      end
    rescue
      print "synth thread failed"
    end
  end
end
end
end
end
end
end
end
end
end
end

define :synth_doCommand do |cmd|
  note = cmd[:note]
  if cmd[:operation] == "note_on"
    #puts note,nv[note]
    noteOn note, 127#cmd[:volume]
  else
    noteOff note
  end
end

define :setSynth do 
  use_synth InstrumentLookup[CurrentInstrument]
end

define :playNote do |note, vol|
  #max duration of note set to 5 on next line. Can increase if you wish.
  node = play note, amp: vol, attack: ENV_Attack , release: ENV_Release, decay: ENV_Decay, sustain: 50,
  attack_level: ENV_Attack_Level, decay_level: ENV_Decay_Level, env_curve: ENV_Curve
  return node
end

define :endRepeatNoteLastNode do |node|
  control node,amp: 0, amp_slide: 0.01
  killListNode  = (killList.select {|n| n[:node] == node}).first
  if killListNode != nil
    killListNode[:releaseVal] = 0.01
  else
    print "failed to find kill node for repeat press"
  end
end

define :noteOn do |note, vol|
  nodeData = ns[note]
  if nodeData[:onStatus] == 0 #check if new start for the note
    #print "set on"
    if nodeData[:node] #kill node for this note as it will bw replaced
      endRepeatNoteLastNode nodeData[:node]
      cue :Cleanup
    end
    setSynth
    
    node = playNote note, vol/127.0
    ns[note] = {node: node, onStatus: 1}
  end
end

define :noteOff do |note|
  nodeData = ns[note]
  if nodeData[:onStatus] == 1 #check if this pitch is on
    nodeData[:onStatus] = 0 #set this pitch off
    #print ns[note]
    node = nodeData[:node]
    if node
      control node,amp: 0, amp_slide: ENV_Release #fade note out in 0.02 seconds
      killList << {node: node, timestamp: Time.now, releaseVal: ENV_Release}
    end
    cue :Cleanup
  end
end

##########################################################################
#                           Drum Logic                                   #
##########################################################################
in_thread(name: :play_drums) do
  loop do
    use_real_time
    sync :PlayDrumsSync
    begin
      while MidiDrumQueue.length > 0 do
          drums_doCommand MidiDrumQueue.deq
      end
    rescue
      print "drums failed"
    end
  end
end

define :drums_doCommand do |cmd|
  note = cmd[:note]
  if cmd[:operation] == "note_on"
    playDrums note, cmd[:volume]
  end
end

define :playDrums do |note, velocity|
  if note == 35
    drums_playBass velocity
  elsif note == 38
    drums_playSnare velocity
  elsif note == 42
    drums_playHighhat velocity
  elsif note == 49
    drums_playSplash velocity
  elsif note == 50
    drums_playAlt velocity
  end
end

define :drums_playSplash do |velocity|
  drums_playMultiSample :drum_splash_soft, :drum_splash_hard, velocity
end

define :drums_playSnare do |velocity|
  drums_playMultiSample :drum_snare_soft, :drum_snare_hard, velocity
end

define :drums_playHighhat do |velocity|
  drums_playSample :drum_cymbal_closed, velocity
end

define :drums_playAlt do |velocity|
  drums_playSample :drum_tom_hi_hard, velocity
end

define :drums_playBass do |velocity|
  drums_playSample :drum_bass_hard, velocity
end

define :drums_playMultiSample do |softHit, hardHit, velocity|
  if velocity < 60
    sample softHit, amp: (velocity/60.0)*2
  else
    sample hardHit, amp: (((velocity-60)/67.0)*0.75+0.25)*2
  end
end
define :drums_playSample do |drumSample, velocity|
  sample drumSample, amp: (velocity/127.0)*2
end

##########################################################################
#                           Node Cleanup                                 #
##########################################################################
#Node cleanup
#Kill nodes when done making sounds. Kill oldest when count exceeds 9
in_thread do
  loop do
    use_real_time
    begin
      sync :Cleanup

      if killList.length > MAX_NODES
        expiredNode  = (killList.select {|n| (Time.now - n[:timestamp]) > n[:releaseVal]}).first
        if expiredNode != nil      
            kill expiredNode[:node]
            killList.delete(expiredNode)
        else
          kill killList.first[:node]
          killList.shift
        end
      end
    rescue
      print "cleanup failed"      
    end
  end
end
