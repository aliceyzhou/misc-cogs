import discord
import calendar
import math
import time
from dateutil import tz
class BadUserHelper:
    bad_role_text = '''Hello, you were assigned the role "{}" in the server "{}".
This role is usually assigned by the mods because you were not following server rules recently, though the reason may vary on a case-by-case basis. The mods will likely contact you shortly regarding the situation.
    
Attempting to remove this role yourself, e.g. by leaving and rejoining the server, will result in punishment. Do not do this.'''
    
    def get_info_embed(member, title, strikes=None, role=None, banned=False):
        embed = discord.Embed(title=title)
        embed.add_field(name="Info", value='''
                        **User**: {}
                        **Name**: {}
                        **Nick**: {}
                        **ID**: {}
                        **Joined**: {}
                        {}{}{}
                        '''.format(member.mention,
                            member.name,
            member.display_name,
            member.id,
            '<t:{}:f>'.format(math.floor(calendar.timegm(member.joined_at.timetuple()))) if isinstance(member, discord.Member) else 'N/A',
            ("**Banned**: \N{HAMMER} BANNED\n" if banned else ""),
            (f"**Role**: {role.mention}\n" if role is not None else ""), 
            (f"**Strikes**: {strikes}\n" if strikes is not None else "")))
        embed.set_thumbnail(url=str(member.default_avatar))
        return embed
    
    def get_latest_messages_embed(latest_messages, member):
        if len(latest_messages) == 0:
            return None
        embed = discord.Embed()
        all = "*Timestamps are PST/PDT*"
        while latest_messages:
            msg = latest_messages.pop()
            clean = msg.clean_content[:200] + ("..." if len(msg.clean_content)>200 else "")
                                    
            result = '[{}]({}) {}: {}'.format(BadUserHelper.get_timestamp(msg.created_at),
                                            msg.jump_url,
                                            msg.channel.mention,
                                            clean)
            if len(all + result) > 4000:
                latest_messages.append(msg)
                break
            all = all + "\n" + result
        embed.description = all
        return embed
    
    def get_timestamp(timestamp):
        return timestamp.replace(tzinfo=tz.gettz('UTC')).astimezone(tz.gettz('America/Los_Angeles')).strftime("%Y-%m-%d %I:%M %p")