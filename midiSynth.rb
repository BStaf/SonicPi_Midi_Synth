MidiBaseStr = "/midi:*:*:*"

RLPF_Res = 0.5
RLPF_Cutoff = 100
ENV_Attack = 0
ENV_Release = 1

MAX_NODES = 9

MidiSynthQueue = Queue.new #queued midi events for synth
MidiDrumQueue = Queue.new #queued midi events for drums

ns = [] #array to store note playing references
killList = []
FxNode = nil

128.times do |i|
  ns[i] = {node: nil, onStatus: 0}
end

InstrumentLookup = { 0 => :piano, 1 => :prophet, 2 => :blade, 3 => :tb303, 4 => :mod_fm }
CurrentInstrument = 1

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
      cue :PlaySynthSync
    end
  end
end

in_thread(name: :read_midiControl) do
  loop do
    use_real_time
    cntrlNum, value = sync MidiBaseStr + "/control_change"
    cmd = getMidiCntrlObjFromMidiInput cntrlNum, value, MidiBaseStr
    setControlSettings cmd[:controlNum], cmd[:value]
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
  if cntrlNum == 16
    RLPF_Res = scaleMidiAi cntrlValue, 0, 0.9
  elsif cntrlNum == 17
    RLPF_Cutoff = scaleMidiAi cntrlValue, 50, 130
  elsif cntrlNum == 18
    ENV_Attack = scaleMidiAi cntrlValue, 0, 1
  elsif cntrlNum == 19
    ENV_Release = scaleMidiAi cntrlValue, 0, 2
  end
  #control FxNode, res: RLPF_Res, cutoff: RLPF_Cutoff
end

##########################################################################
#                            Play Synth                                  #
##########################################################################
#Midi controls thread
with_fx :rlpf do |fxnode|
  in_thread(name: :play_synth) do
    FxNode = fxnode
    loop do
      use_real_time
      sync :PlaySynthSync
      begin
        control fxnode, res: RLPF_Res, cutoff: RLPF_Cutoff
        while MidiSynthQueue.length > 0 do
          synth_doCommand MidiSynthQueue.deq
        end
      rescue
        print "synth failed"
      end
    end
  end
end

define :synth_doCommand do |cmd|
  note = cmd[:note]
  if cmd[:operation] == "note_on"
    #puts note,nv[note]
    noteOn note, cmd[:volume]
  else
    noteOff note
  end
end

define :setSynth do 
  use_synth InstrumentLookup[CurrentInstrument]
end

define :noteOn do |note, vol|
  nodeData = ns[note]
  if nodeData[:onStatus] == 0 #check if new start for the note
    #print "set on"
    if nodeData[:node] #kill node for this note as it will bw replaced
      kill nodeData[:node]
      #print "note killed"
    end
    setSynth
    #max duration of note set to 5 on next line. Can increase if you wish.
    node = play note, amp: (vol / 127.0), attack: ENV_Attack , release: 1, sustain: 50 #play note
    #print "note played"
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
      killList << {node: node, timestamp: Time.now}
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
      item = killList.first
      if item != nil
        timeDiff = Time.now - item[:timestamp]
        if killList.length > MAX_NODES || timeDiff > ENV_Release
          #print "kill"
          kill item[:node]
          killList.shift
        end
      end
    rescue
      print "cleanup failed"      
    end
  end
end
