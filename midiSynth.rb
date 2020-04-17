#MidiControlDevice = "/midi:*:*:*"#"/midi:arduino_leonardo:0:1"
MidiBaseStr = "/midi:*:*:*"

RLPF_Res = 0.5
RLPF_Cutoff = 100
ENV_Attack = 0
ENV_Release = 1

MAX_NODES = 8

MidiSynthQueue = Queue.new #queued midi events for synth
MidiDrumQueue = Queue.new #queued midi events for drums

ns=[] #array to store note playing references
nv=[0]*128 #array to store state of note for a particlar pitch 1=on, 0 = 0ff
killList=[] #list of nodes that will need to be killed when finished

128.times do |i|
  ns[i]=("n"+i.to_s).to_sym #set up array of symbols :n0 ...:n127
end

########################################################
# handle midi control input currently 16 - 19
########################################################
define :scaleMidiAi do |rawVal, lowEu, highEu|
  val = (rawVal/127.0) * (highEu - lowEu) + lowEu
  return val
end

define :setControlSettings do |cntrlSet|
  if cntrlSet[0] == 16
    RLPF_Res = scaleMidiAi cntrlSet[1], 0, 0.9
  elsif cntrlSet[0] == 17
    RLPF_Cutoff = scaleMidiAi cntrlSet[1], 50, 130
  elsif cntrlSet[0] == 18
    ENV_Attack = scaleMidiAi cntrlSet[1], 0, 1
  elsif cntrlSet[0] == 19
    ENV_Release = scaleMidiAi cntrlSet[1], 0, 2
  end
end

define :getControlChange do |midiDevice|
  cntrl = sync midiDevice+"/control_change"
  return [cntrl[0],cntrl[1]]
end

#Midi controls thread
in_thread do
  loop do
    use_real_time
    setControlSettings(getControlChange(MidiBaseStr))
    sleep 0.02
  end
end
########################################################
# Midi keyboard Logic
########################################################
define :getMidiCntrlObjFromMidiInput do |midiBase|
  note, vol = sync midiBase + "/note_*"
  vol = vol*0.75
  #get_event may be depricated in the future.
  #split event by ',' and grab the element that contains the midi command
  command = get_event(midiBase + "/*").to_s.split(",")[6]
  #print command[3..-2].split(":").last
  #get the last part of the command string
  channel_operation = command[3..-2].split(":").last.split("/")
  return {note: note, volume: vol, operation: channel_operation[1], channel: channel_operation[0]}
end

define :midiInputHandler do |midiBase|
  #wait for midi note command
  cmd = getMidiCntrlObjFromMidiInput midiBase
  print cmd
  #print cmd[:channel]
  if cmd[:channel] == "10"
    MidiDrumQueue << cmd
  else
    MidiSynthQueue << cmd
  end
end

define :noteOn do |note, vol|
  node = get(ns[note])
  
  if nv[note]==0 #check if new start for the note
    nv[note]=1 #mark note as started for this pitch
    
    if node #kill node for this note as it will bw replaced
      kill node
    end
    
    use_synth :prophet
    #max duration of note set to 5 on next line. Can increase if you wish.
    node = play note, amp: (vol / 127.0), attack: ENV_Attack , release: 1, sustain: 50 #play note
    
    set ns[note],node #store reference in ns array
  end
end

define :noteOff do |note|
  node = get(ns[note])
  if nv[note]==1 #check if this pitch is on
    nv[note]=0 #set this pitch off
    if node
      control node,amp: 0, amp_slide: ENV_Release #fade note out in 0.02 seconds
      killList << {node: node, timestamp: Time.now}
    end
  end
end
########################################################
# Drum Logic
########################################################
define :playDrums do |note, velocity|
  if note == 50
    drums_playBass velocity
  elsif note == 42
    drums_playSnare velocity
  elsif note == 49
    drums_playHighhat velocity
  elsif note == 38
    drums_playSplash velocity
  elsif note == 35
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
    sample softHit, amp: velocity/60.0
  else
    sample hardHit, amp: (((velocity-60)/67.0)*0.75+0.25)
  end
end
define :drums_playSample do |drumSample, velocity|
  sample drumSample, amp: (velocity/127.0)
end

define :synth_doCommand do |cmd|
  note = cmd[:note]
  if cmd[:operation] == "note_on"
    puts note,nv[note]
    noteOn note, cmd[:volume]
  else
    noteOff note
  end
end

define :drums_doCommand do |cmd|
  note = cmd[:note]
  if cmd[:operation] == "note_on"
    playDrums note, cmd[:volume]
  end
end

live_loop :midi_read do
  use_real_time
  midiInputHandler MidiBaseStr
end

#Midi controls thread
with_fx :rlpf, res: RLPF_Res, cutoff: RLPF_Cutoff do
  live_loop :play_synth do
    use_real_time
    begin
      sleep 0.02
      
      if MidiSynthQueue.length > 0
        synth_doCommand MidiSynthQueue.deq
      end
    rescue
      print "synth failed"
    end
  end
end

live_loop :play_drums do
  use_real_time
  begin
    sleep 0.02
    if MidiDrumQueue.length > 0
      drums_doCommand MidiDrumQueue.deq
    end
  rescue
    print "drums failed"
  end
end


#Node cleanup
#Kill nodes when done making sounds. Kill oldest when count exceeds 9
in_thread do
  loop do
    begin
      sleep 0.05
      item = killList.first
      if item != nil
        timeDiff = Time.now - item[:timestamp]
        if killList.length > MAX_NODES || timeDiff > ENV_Release
          kill item[:node]
          killList.shift
        end
      end
    rescue
      print "cleanup failed"
      
    end
  end
end