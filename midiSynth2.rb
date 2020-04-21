MidiBaseStr = "/midi:*:*:*"

RLPF_Res = 0.5
RLPF_Cutoff = 100
ENV_Attack = 0
ENV_Release = 1

MidiSynthQueue = Queue.new #queued midi events for synth
MidiDrumQueue = Queue.new #queued midi events for drums

ns = [] #array to store note playing references

##########################################################################
#                      Read Midi Commands                                #
##########################################################################
define :midiInputHandler do |midiBase|
  #wait for midi note command
  cmd = getMidiCntrlObjFromMidiInput midiBase
  print cmd
  #print cmd[:channel]
  if cmd[:channel] == "10"
    MidiDrumQueue << cmd
    cue :PlaySynthSync
  else
    MidiSynthQueue << cmd
  end
end

define :getMidiCntrlObjFromMidiInput do |midiBase|
  note, vol = sync midiBase + "/note_*"
  #get_event may be depricated in the future.
  #split event by ',' and grab the element that contains the midi command
  command = get_event(midiBase + "/*").to_s.split(",")[6]
  #print command[3..-2].split(":").last
  #get the last part of the command string
  channel_operation = command[3..-2].split(":").last.split("/")
  return {note: note, volume: vol, operation: channel_operation[1], channel: channel_operation[0]}
end

##########################################################################
#                            Play Synth                                  #
##########################################################################
#Midi controls thread
#with_fx :rlpf, res: RLPF_Res, cutoff: RLPF_Cutoff do |fxnode|
with_fx :rlpf do |fxnode|
  in_thread (name: :play_synth) do
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

define :synth_doCommand do |cmd|
  note = cmd[:note]
  if cmd[:operation] == "note_on"
    puts note,nv[note]
    noteOn note, cmd[:volume]
  else
    noteOff note
  end
end

define :setSynth do
  #use_synth :prophet
  use_synth :piano #blade tb303 #piano #mod_fm #prophet
end

define :noteOn do |note, vol|
  nodeData = get(ns[note])
  if nodeData[:onStatus] == 0 #check if new start for the note

    if nodeData[:node] #kill node for this note as it will bw replaced
      kill nodeData[:node]
    end
    
    setSynth #set synth instrument
    #max duration of note set to 5 on next line. Can increase if you wish.
    node = play note, amp: (vol / 127.0), attack: ENV_Attack , release: 1, sustain: 50 #play note
    
    set ns[note], {node: node, onStatus: 1}
  end
end

define :noteOff do |note|
  nodeData = get(ns[note])
  if nodeData[:onStatus] == 1 #check if this pitch is on
    nodeData[:onStatus] == 0 #set this pitch off

    node = nodeData[:node]
    if node
      control node,amp: 0, amp_slide: ENV_Release #fade note out in 0.02 seconds
      killList << {node: node, timestamp: Time.now}
    end
  end
end
  
# live_loop :play_drums do
#   use_real_time
#   begin
#     sleep 0.01
#     while MidiDrumQueue.length > 0 do
#         drums_doCommand MidiDrumQueue.deq
#       end
#     rescue
#       print "drums failed"
#     end
#   end
    
##########################################################################
#                           Node Cleanup                                 #
##########################################################################
#Node cleanup
#Kill nodes when done making sounds. Kill oldest when count exceeds 9
in_thread do
  loop do
    use_real_time
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