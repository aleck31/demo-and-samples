#!/usr/bin/env python3
"""
Amazon Polly Interactive Demo Script

This script provides an interactive interface to:
1. Select voice engine (neural, standard, generative, long-form)
2. Choose language and voice
3. Input custom text or use sample text
4. Generate and play speech in real-time
"""

import os
import sys
import tempfile
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


class PollyDemo:
    def __init__(self):
        self.client = None
        self.voices_data = {}
        self.languages_dir = Path("./languages")
        self.temp_dir = Path(tempfile.gettempdir())
        
    def initialize_client(self) -> bool:
        """Initialize AWS Polly client"""
        try:
            self.client = boto3.Session(region_name='us-east-1').client('polly')
            # Test connection with a simple call
            self.client.describe_voices()
            return True
        except NoCredentialsError:
            print("❌ AWS credentials not found. Please configure your AWS credentials.")
            return False
        except Exception as e:
            print(f"❌ Failed to initialize AWS Polly client: {e}")
            return False
    
    def load_voices(self) -> bool:
        """Load available voices from AWS Polly"""
        try:
            print("🔄 Loading available voices...")
            response = self.client.describe_voices()
            
            for voice in response['Voices']:
                lang_name = voice['LanguageName']
                if lang_name not in self.voices_data:
                    self.voices_data[lang_name] = []
                
                self.voices_data[lang_name].append({
                    'id': voice['Id'],
                    'name': voice['Name'],
                    'gender': voice['Gender'],
                    'engines': voice['SupportedEngines'],
                    'language_code': voice['LanguageCode']
                })
            
            print(f"✅ Loaded {len(response['Voices'])} voices in {len(self.voices_data)} languages")
            return True
        except Exception as e:
            print(f"❌ Failed to load voices: {e}")
            return False
    
    def get_available_engines(self) -> List[str]:
        """Get all available engines from loaded voices"""
        engines = set()
        for voices in self.voices_data.values():
            for voice in voices:
                engines.update(voice['engines'])
        return sorted(list(engines))
    
    def select_engine(self) -> Optional[str]:
        """Let user select voice engine"""
        engines = self.get_available_engines()
        
        print("\n🎛️  Available Voice Engines:")
        for i, engine in enumerate(engines, 1):
            description = {
                'neural': 'High-quality neural voices',
                'standard': 'Traditional concatenative synthesis',
                'generative': 'Most human-like, emotionally engaged',
                'long-form': 'Optimized for longer content'
            }.get(engine, 'Advanced voice engine')
            
            print(f"  {i}. {engine.capitalize()} - {description}")
        
        while True:
            try:
                choice = input(f"\nSelect engine (1-{len(engines)}) or 'q' to quit: ").strip()
                if choice.lower() == 'q':
                    return None
                
                index = int(choice) - 1
                if 0 <= index < len(engines):
                    return engines[index]
                else:
                    print(f"❌ Please enter a number between 1 and {len(engines)}")
            except ValueError:
                print("❌ Please enter a valid number")
    
    def get_voices_for_engine(self, engine: str) -> Dict[str, List]:
        """Get voices that support the selected engine"""
        filtered_voices = {}
        for lang_name, voices in self.voices_data.items():
            lang_voices = [v for v in voices if engine in v['engines']]
            if lang_voices:
                filtered_voices[lang_name] = lang_voices
        return filtered_voices
    
    def select_language_and_voice(self, engine: str) -> Optional[Tuple[str, Dict]]:
        """Let user select language and voice"""
        available_voices = self.get_voices_for_engine(engine)
        
        if not available_voices:
            print(f"❌ No voices available for {engine} engine")
            return None
        
        # Display languages
        languages = list(available_voices.keys())
        print(f"\n🌍 Available Languages for {engine.capitalize()} Engine:")
        for i, lang in enumerate(languages, 1):
            voice_count = len(available_voices[lang])
            print(f"  {i}. {lang} ({voice_count} voice{'s' if voice_count > 1 else ''})")
        
        # Select language
        while True:
            try:
                choice = input(f"\nSelect language (1-{len(languages)}) or 'b' to go back: ").strip()
                if choice.lower() == 'b':
                    return None
                
                lang_index = int(choice) - 1
                if 0 <= lang_index < len(languages):
                    selected_lang = languages[lang_index]
                    break
                else:
                    print(f"❌ Please enter a number between 1 and {len(languages)}")
            except ValueError:
                print("❌ Please enter a valid number")
        
        # Display voices for selected language
        voices = available_voices[selected_lang]
        print(f"\n🎤 Available Voices for {selected_lang}:")
        for i, voice in enumerate(voices, 1):
            print(f"  {i}. {voice['name']} ({voice['gender']}) - {voice['id']}")
        
        # Select voice
        while True:
            try:
                choice = input(f"\nSelect voice (1-{len(voices)}) or 'b' to go back: ").strip()
                if choice.lower() == 'b':
                    return None
                
                voice_index = int(choice) - 1
                if 0 <= voice_index < len(voices):
                    return selected_lang, voices[voice_index]
                else:
                    print(f"❌ Please enter a number between 1 and {len(voices)}")
            except ValueError:
                print("❌ Please enter a valid number")
    
    def get_sample_texts(self) -> Dict[str, str]:
        """Load sample texts from languages directory"""
        samples = {}
        if not self.languages_dir.exists():
            return samples
        
        for file_path in self.languages_dir.glob("*.txt"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        lang_name = file_path.stem
                        samples[lang_name] = content
            except Exception as e:
                print(f"⚠️  Warning: Could not read {file_path}: {e}")
        
        return samples
    
    def select_text_content(self, language: str) -> Optional[str]:
        """Let user select text content"""
        samples = self.get_sample_texts()
        
        print(f"\n📝 Text Input Options:")
        print("  1. Use sample text")
        
        # Find matching sample text
        matching_samples = []
        for sample_name, content in samples.items():
            if language.lower() in sample_name.lower() or sample_name.lower() in language.lower():
                matching_samples.append((sample_name, content))
        
        if matching_samples:
            for i, (name, content) in enumerate(matching_samples):
                preview = content[:50] + "..." if len(content) > 50 else content
                print(f"     • {name}: {preview}")
        
        print("  2. Enter custom text")
        
        while True:
            choice = input(f"\nSelect option (1-2) or 'b' to go back: ").strip()
            if choice.lower() == 'b':
                return None
            elif choice == '1' and matching_samples:
                if len(matching_samples) == 1:
                    return matching_samples[0][1]
                else:
                    # Multiple samples, let user choose
                    print("\nAvailable samples:")
                    for i, (name, content) in enumerate(matching_samples, 1):
                        preview = content[:100] + "..." if len(content) > 100 else content
                        print(f"  {i}. {name}: {preview}")
                    
                    while True:
                        try:
                            sample_choice = input(f"Select sample (1-{len(matching_samples)}): ").strip()
                            sample_index = int(sample_choice) - 1
                            if 0 <= sample_index < len(matching_samples):
                                return matching_samples[sample_index][1]
                            else:
                                print(f"❌ Please enter a number between 1 and {len(matching_samples)}")
                        except ValueError:
                            print("❌ Please enter a valid number")
            elif choice == '1' and not matching_samples:
                print("❌ No sample text available for this language. Please choose option 2.")
            elif choice == '2':
                text = input("\n📝 Enter your text: ").strip()
                if text:
                    return text
                else:
                    print("❌ Please enter some text")
            else:
                print("❌ Please select a valid option")
    
    def synthesize_speech(self, text: str, voice_id: str, language_code: str, engine: str) -> Optional[str]:
        """Synthesize speech and return path to audio file"""
        try:
            print("🔄 Generating speech...")
            
            # Wrap text in SSML if it's not already
            if not text.strip().startswith('<speak>'):
                ssml_text = f'<speak>\n\t{text}\n</speak>'
            else:
                ssml_text = text
            
            response = self.client.synthesize_speech(
                VoiceId=voice_id,
                LanguageCode=language_code,
                OutputFormat='mp3',
                Text=ssml_text,
                TextType='ssml',
                Engine=engine
            )
            
            # Save to temporary file
            temp_file = self.temp_dir / f"polly_demo_{voice_id}_{engine}.mp3"
            with open(temp_file, 'wb') as f:
                f.write(response['AudioStream'].read())
            
            print("✅ Speech generated successfully!")
            return str(temp_file)
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'InvalidParameterValue':
                print("❌ Invalid parameter. Please check your text content.")
            elif error_code == 'TextLengthExceededException':
                print("❌ Text is too long. Please use shorter text.")
            else:
                print(f"❌ AWS Error: {e}")
            return None
        except Exception as e:
            print(f"❌ Failed to synthesize speech: {e}")
            return None
    
    def play_audio(self, audio_file: str) -> bool:
        """Play audio file using Python audio libraries"""
        try:
            print(f"🔊 Playing audio...")
            
            # Try pygame first (most reliable and maintained)
            try:
                import pygame
                pygame.mixer.init()
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
                
                # Wait for playback to complete
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                
                pygame.mixer.quit()
                return True
                
            except ImportError:
                print("💡 pygame not found, trying system players...")
            except Exception as e:
                error_msg = str(e).lower()
                if 'audio device' in error_msg or 'dsp' in error_msg or 'alsa' in error_msg:
                    print(f"💡 No audio device available ({e}), trying system players...")
                else:
                    print(f"💡 pygame failed ({e}), trying system players...")
            
            # Fallback to system players
            if sys.platform.startswith('linux'):
                # Try common Linux audio players
                players = ['mpg123', 'mpv', 'vlc', 'aplay', 'paplay']
                for player in players:
                    if subprocess.run(['which', player], capture_output=True).returncode == 0:
                        try:
                            subprocess.run([player, audio_file], check=True, capture_output=True)
                            return True
                        except subprocess.CalledProcessError:
                            continue  # Try next player
                
                print("❌ No audio playback method available.")
                print("   This might be due to:")
                print("   • No audio device/sound card available")
                print("   • Running in a headless environment")
                print("   • Audio system not properly configured")
                print(f"💾 Audio file saved to: {audio_file}")
                print("   You can download and play it manually.")
                return False
                
            elif sys.platform == 'darwin':  # macOS
                subprocess.run(['afplay', audio_file], check=True)
                return True
                
            elif sys.platform.startswith('win'):  # Windows
                os.startfile(audio_file)
                return True
                
            else:
                print(f"❌ Unsupported platform: {sys.platform}")
                print(f"💾 Audio file saved to: {audio_file}")
                return False
                
        except subprocess.CalledProcessError:
            print("❌ Failed to play audio")
            print(f"💾 Audio file saved to: {audio_file}")
            return False
        except Exception as e:
            print(f"❌ Error playing audio: {e}")
            print(f"💾 Audio file saved to: {audio_file}")
            return False
    
    def cleanup_temp_files(self):
        """Clean up temporary audio files"""
        try:
            for file_path in self.temp_dir.glob("polly_demo_*.mp3"):
                file_path.unlink()
        except Exception:
            pass  # Ignore cleanup errors
    
    def run(self):
        """Main demo loop"""
        print("🎵 Amazon Polly Interactive Demo")
        print("=" * 40)
        
        # Initialize
        if not self.initialize_client():
            return
        
        if not self.load_voices():
            return
        
        try:
            while True:
                print("\n" + "=" * 40)
                
                # Select engine
                engine = self.select_engine()
                if engine is None:
                    break
                
                # Select language and voice
                selection = self.select_language_and_voice(engine)
                if selection is None:
                    continue
                
                language, voice = selection
                
                # Select text content
                text = self.select_text_content(language)
                if text is None:
                    continue
                
                # Show summary
                print(f"\n📋 Summary:")
                print(f"   Engine: {engine}")
                print(f"   Language: {language}")
                print(f"   Voice: {voice['name']} ({voice['gender']})")
                print(f"   Text: {text[:100]}{'...' if len(text) > 100 else ''}")
                
                confirm = input("\n🎯 Generate and play? (y/n): ").strip().lower()
                if confirm != 'y':
                    continue
                
                # Generate speech
                audio_file = self.synthesize_speech(
                    text, voice['id'], voice['language_code'], engine
                )
                
                if audio_file:
                    # Play audio
                    if self.play_audio(audio_file):
                        print("✅ Playback completed!")

                # Ask if user wants to continue
                continue_demo = input("\n🔄 Try another voice? (y/n): ").strip().lower()
                if continue_demo != 'y':
                    break
                    
        except KeyboardInterrupt:
            print("\n\n👋 Demo interrupted by user")
        finally:
            self.cleanup_temp_files()
            print("🧹 Cleaned up temporary files")
            print("👋 Thanks for using Amazon Polly Demo!")


def main():
    """Main entry point"""
    demo = PollyDemo()
    demo.run()


if __name__ == "__main__":
    main()
