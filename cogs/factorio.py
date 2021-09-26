# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import asyncio

from discord.ext.commands.core import command
import json

import config
import aws.ec2.manage


class Factorio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def create_msg_embed(self, run_name, msg):
        embed = discord.Embed()
        embed.color = discord.Color.blue()
        embed.add_field(name=run_name, value=msg)
        return embed

    @commands.is_owner()
    @commands.command()
    async def reload(self, ctx, module_name):
        await ctx.send(f'モジュール {module_name} の再読み込みを開始')
        try:
            self.bot.reload_extension(module_name)
            await ctx.send(f'モジュール {module_name} の再読み込みを終了')
        except (commands.errors.ExtensionNotLoaded,
                commands.errors.ExtensionNotFound,
                commands.errors.NoEntryPointError,
                commands.errors.ExtensionFailed) as e:
            await ctx.send(f'モジュール {module_name} の再読み込みに失敗。{e}')
            return

    @commands.command()
    async def factorio_start_srv(self, ctx, srv_name: str = 'gae_bulg_k2'):
        srv_list = config.srv_list
        await ctx.send(f'サーバー {srv_name} を起動します')
        for srv in srv_list:
            if srv['name'] != srv_name:
                continue
            if srv['type'] != 'ec2':
                await ctx.send(f'Error: サーバー {srv_name} は、EC2インスタンスではありません。停止処理を終了します。')
                return
            try:
                rp = aws.ec2.manage.start_instance(srv['instance_id'])
                await ctx.send(f'サーバー {srv_name} を起動しました')
                return
            except Exception as e:
                await ctx.send('Error: サーバー {srv_name} を起動中にエラーが発生しました。' + str(e))
                return

        await ctx.send(f'Notice: サーバー {srv_name} は管理外です。起動処理を終了します。')

    @factorio_start_srv.error
    async def start_srv_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send(f'コマンドのパラメータの形式が間違っています')
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f'コマンドのパラメータの数が足りません')

    @commands.command()
    async def factorio_stop_srv(self, ctx, srv_name: str = 'gae_bulg_k2'):
        srv_list = config.srv_list
        await ctx.send(f'サーバー {srv_name} を停止します')

        for srv in srv_list:
            if srv['name'] != srv_name:
                continue
            if srv['type'] != 'ec2':
                await ctx.send(f'Error: サーバー {srv_name} は、EC2インスタンスではありません。停止処理を終了します。')
                return
            try:
                rp = aws.ec2.manage.stop_instance(srv['instance_id'])
                await ctx.send(f'サーバー {srv_name} を停止しました')
                return
            except Exception as e:
                await ctx.send('Error: サーバー {srv_name} を停止中にエラーが発生しました。' + str(e))
                return
        await ctx.send(f'Notice: サーバー {srv_name} は管理外です。停止処理を終了します。')

    @commands.command()
    async def factorio_status(self, ctx):
        srv_list = config.srv_list
        msg = 'サーバーの状態\n\n'
        for srv in srv_list:
            if srv['type'] != 'ec2' or 'instance_id' not in srv.keys():
                continue

            msg += srv['name']
            try:
                rp = aws.ec2.manage.status_instance(srv['instance_id'])
                if rp['InstanceStatuses']:
                    for st in rp['InstanceStatuses']:
                        if srv['instance_id'] != st['InstanceId']:
                            continue

                        if st['InstanceState']['Name'] == 'running':
                            msg += '\t'
                            msg += '起動中 (running)'
                else:
                    msg += '\t'
                    msg += '停止中 (stopping)'
            except Exception as e:
                msg += str(e)

            msg += '\n\n'

        msg_embed = self.create_msg_embed('status', msg)
        await ctx.send(embed=msg_embed)


def setup(bot):
    bot.add_cog(Factorio(bot))
