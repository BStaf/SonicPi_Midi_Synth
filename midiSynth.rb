MidiBaseStr = "/midi:*:*"

Settings = {:Compressor_Clamp_Time=>{:midi=>104,:val=>0.01,:min=>0,:max=>10},:Compressor_Mix=>{:midi=>92,:val=>0,:min=>0,:max=>1},:Compressor_Relax_Time=>{:midi=>107,:val=>0.01,:min=>0,:max=>10},
:Compressor_Slope_Above=>{:midi=>105,:val=>0.5,:min=>0,:max=>10},:Compressor_Slope_Below=>{:midi=>106,:val=>1,:min=>0,:max=>10},:Compressor_Threshold=>{:midi=>103,:val=>0.2,:min=>0,:max=>10},
:Distortion_Distort=>{:midi=>116,:val=>0.5,:min=>0,:max=>0.99},:Distortion_Mix=>{:midi=>95,:val=>0,:min=>0,:max=>1},:Echo_Decay=>{:midi=>101,:val=>2,:min=>0.1,:max=>10},
:Echo_Max_Phase=>{:midi=>102,:val=>2,:min=>0.1,:max=>10},:Echo_Mix=>{:midi=>91,:val=>0,:min=>0,:max=>1},:Echo_Phase=>{:midi=>100,:val=>0.25,:min=>0.1,:max=>10},
:Flanger_Decay=>{:midi=>121,:val=>2,:min=>0,:max=>10},:Flanger_Delay=>{:midi=>119,:val=>5,:min=>0,:max=>10},:Flanger_Depth=>{:midi=>120,:val=>5,:min=>0,:max=>10},
:Flanger_Feedback=>{:midi=>122,:val=>0,:min=>0,:max=>10},:Flanger_Mix=>{:midi=>97,:val=>0,:min=>0,:max=>1},:Flanger_Phase=>{:midi=>117,:val=>4,:min=>0.1,:max=>10},
:Flanger_Pulse_Flanger_Width=>{:midi=>118,:val=>0.5,:min=>0,:max=>1},:Octaver_Mix=>{:midi=>96,:val=>0,:min=>0,:max=>1},:Reverb_Damp=>{:midi=>99,:val=>0.5,:min=>0,:max=>1},
:Reverb_Mix=>{:midi=>90,:val=>0,:min=>0,:max=>1},:Reverb_Room=>{:midi=>98,:val=>0.6,:min=>0,:max=>1},:Rlpf_Cutoff=>{:midi=>114,:val=>100,:min=>0,:max=>100},
:Rlpf_Mix=>{:midi=>94,:val=>0,:min=>0,:max=>1},:Rlpf_Res=>{:midi=>115,:val=>0.5,:min=>0,:max=>0.99},:Whammy_Deltime=>{:midi=>110,:val=>0.05,:min=>0,:max=>2},
:Whammy_Grainsize=>{:midi=>111,:val=>0.075,:min=>0,:max=>2},:Whammy_Max_Delay_Time=>{:midi=>109,:val=>1,:min=>0,:max=>10},:Whammy_Mix=>{:midi=>93,:val=>0,:min=>0,:max=>1},
:Whammy_Transpose=>{:midi=>108,:val=>12,:min=>0,:max=>24},
:Attack=>{:midi=>33,:val=>0,:min=>0,:max=>1},:Attack_Level=>{:midi=>36,:val=>1,:min=>0,:max=>1},:Coef=>{:midi=>71,:val=>0.3,:min=>-1,:max=>1},
:Decay=>{:midi=>34,:val=>0,:min=>0,:max=>1},:Decay_Level=>{:midi=>37,:val=>1,:min=>0,:max=>1},:Depth=>{:midi=>46,:val=>1,:min=>0,:max=>20},
:Detune=>{:midi=>43,:val=>0.1,:min=>0,:max=>5},:Detune1=>{:midi=>54,:val=>12,:min=>-24,:max=>24},:Detune2=>{:midi=>55,:val=>24,:min=>-24,:max=>24},
:Divisor=>{:midi=>45,:val=>2,:min=>0,:max=>20},:Dpulse_Width=>{:midi=>44,:val=>0.5,:min=>0,:max=>1},:Hard=>{:midi=>66,:val=>0.5,:min=>0,:max=>1},
:Max_Delay_Time=>{:midi=>69,:val=>0.125,:min=>0.125,:max=>1},:Mod_Phase=>{:midi=>47,:val=>0.25,:min=>0,:max=>5},:Mod_Phase_Offset=>{:midi=>50,:val=>0,:min=>0,:max=>1},
:Mod_Pulse_Width=>{:midi=>49,:val=>0.5,:min=>0,:max=>1},:Mod_Range=>{:midi=>48,:val=>5,:min=>0,:max=>12},:Noise_Amp=>{:midi=>68,:val=>0.8,:min=>0,:max=>1},
:Pluck_Decay=>{:midi=>70,:val=>30,:min=>1,:max=>100},:Pulse_Width=>{:midi=>40,:val=>0.5,:min=>0,:max=>1},:Release=>{:midi=>35,:val=>1,:min=>0,:max=>1},
:Reverb_Time=>{:midi=>59,:val=>100,:min=>0.1,:max=>200},:Ring=>{:midi=>57,:val=>0.2,:min=>0.1,:max=>50},:Room=>{:midi=>58,:val=>70,:min=>0.1,:max=>300},
:Stereo_Width=>{:midi=>67,:val=>0,:min=>0,:max=>1},:Sub_Amp=>{:midi=>41,:val=>1,:min=>0,:max=>2},:Sub_Detune=>{:midi=>42,:val=>-12,:min=>-24,:max=>24},
:Vel=>{:midi=>65,:val=>0.2,:min=>0,:max=>1},:Vibrato_Delay=>{:midi=>63,:val=>0.5,:min=>0,:max=>2},:Vibrato_Depth=>{:midi=>62,:val=>0.15,:min=>0,:max=>5},
:Vibrato_Onset=>{:midi=>64,:val=>0.1,:min=>0,:max=>2},:Vibrato_Rate=>{:midi=>61,:val=>6,:min=>0,:max=>20}}

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
    if cmd[:channel] != "10"
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
  Settings.each do |key, settingData|
    if settingData[:midi] == cntrlNum
      settingData[:val] = scaleMidiAi cntrlValue, settingData[:min], settingData[:max]
    end
  end
  
  if cntrlNum == 32
    PITCH_ADJ = (scaleMidiAi cntrlValue, 0, 12) - 6
    if PITCH_ADJ < 0.1 && PITCH_ADJ > -0.1
      PITCH_ADJ = 0
    end
  elsif cntrlNum == 30
    set_volume! (scaleMidiAi cntrlValue, 0, 1)
  end
  #control FxNode, res: FX_Rlpf_Res, cutoff: FX_rlpf_cutoff
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
 # with_fx :rhpf do |rhpf|
  with_fx :distortion do |distortion|
  with_fx :octaver do |octaver|
  with_fx :flanger do |flanger|
  with_fx :pitch_shift do |pitchShift|#PITCH_ADJ
    in_thread(name: :play_synth) do
      begin
        print "stuff"
        loop do
          use_real_time
          #sync :PlaySynthSync
          begin
            control pitchShift, pitch: PITCH_ADJ
            control rlpf, mix: Settings[:Rlpf_Mix][:val], res: Settings[:Rlpf_Res][:val], cutoff: Settings[:Rlpf_Cutoff][:val]
            control reverb, mix: Settings[:Reverb_Mix][:val], damp: Settings[:Reverb_Damp][:val], room: Settings[:Reverb_Room][:val]
            control echo, mix: Settings[:Echo_Mix][:val], decay: Settings[:Echo_Decay][:val], phase: Settings[:Echo_Phase][:val]#, max_phase: Settings[:Echo_Max_Phase][:val]
            control compressor, mix: Settings[:Compressor_Mix][:val], clamp_time: Settings[:Compressor_Clamp_Time][:val], relax_time: Settings[:Compressor_Relax_Time][:val],
              slope_above: Settings[:Compressor_Slope_Above][:val], slope_below: Settings[:Compressor_Slope_Below][:val], threshold: Settings[:Compressor_Threshold][:val]
            control whammy, mix: Settings[:Whammy_Mix][:val],
              transpose: Settings[:Whammy_Transpose][:val]#,  deltime: Settings[:Whammy_Deltime][:val], grainsize: Settings[:Whammy_Grainsize][:val]max_delay_time: Settings[:Whammy_Max_Delay_Time][:val],
              control distortion, mix: Settings[:Distortion_Mix][:val], distort: Settings[:Distortion_Distort][:val]
            control octaver, mix: Settings[:Octaver_Mix][:val]
            control flanger, mix: Settings[:Flanger_Mix][:val], decay: Settings[:Flanger_Decay][:val], delay: Settings[:Flanger_Delay][:val], depth: Settings[:Flanger_Depth][:val], feedback: Settings[:Flanger_Feedback][:val],
              phase: Settings[:Flanger_Phase][:val], pulse_flanger_width: Settings[:Flanger_Pulse_Flanger_Width][:val]
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
  #end
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
  node = play note, amp: vol, attack: Settings[:Attack][:val], release: Settings[:Release][:val], decay: Settings[:Decay][:val], sustain: 50,
  attack_level: Settings[:Attack_Level][:val], decay_level: Settings[:Decay_Level][:val], env_curve: ENV_Curve, coef: Settings[:Coef][:val], 
  depth: Settings[:Depth][:val], detune: Settings[:Detune][:val], detune1: Settings[:Detune1][:val], detune2: Settings[:Detune2][:val], divisor: Settings[:Divisor][:val], 
  dpulse_width: Settings[:Dpulse_Width][:val], hard: Settings[:Hard][:val], max_delay_time: Settings[:Max_Delay_Time][:val], mod_phase: Settings[:Mod_Phase][:val], 
  mod_phase_offset: Settings[:Mod_Phase_Offset][:val], mod_pulse_width: Settings[:Mod_Pulse_Width][:val], mod_range: Settings[:Mod_Range][:val], 
  noise_amp: Settings[:Noise_Amp][:val], pluck_decay: Settings[:Pluck_Decay][:val], pulse_width: Settings[:Pulse_Width][:val], 
  reverb_time: Settings[:Reverb_Time][:val], ring: Settings[:Ring][:val], room: Settings[:Room][:val], stereo_width: Settings[:Stereo_Width][:val], 
  sub_amp: Settings[:Sub_Amp][:val], sub_detune: Settings[:Sub_Detune][:val], vel: Settings[:Vel][:val], vibrato_delay: Settings[:Vibrato_Delay][:val], 
  vibrato_depth: Settings[:Vibrato_Depth][:val], vibrato_onset: Settings[:Vibrato_Onset][:val], vibrato_rate: Settings[:Vibrato_Rate][:val]

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
    node = nodeData[:node]
    if node
      control node,amp: 0, amp_slide: Settings[:Release][:val] #fade note out in 0.02 seconds
      killList << {node: node, timestamp: Time.now, releaseVal: Settings[:Release][:val]}
    end
    cue :Cleanup
  end
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
