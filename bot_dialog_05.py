from botbuilder.core import ConversationState, TurnContext, ActivityHandler, MessageFactory
from botbuilder.dialogs import DialogSet, WaterfallDialog, WaterfallStepContext
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, PromptOptions, PromptValidatorContext

class BotDialog(ActivityHandler):

    def __init__(self, conversation: ConversationState):
        self.con_statea = conversation
        self.state_prop = self.con_statea.create_property('dialog_set')
        self.dialog_set = DialogSet(self.state_prop)
        self.dialog_set.add(TextPrompt('text_prompt'))
        self.dialog_set.add(NumberPrompt('number_prompt', self.isValidNumber))
        self.dialog_set.add(WaterfallDialog('main_dialog',[self.GetUserName,self.GetUserNumber,self.GetUserEmailId,
                                                                                 self.GetUserIntention,self.Completed]))

    async def isValidNumber(self, prompt_valid:PromptValidatorContext):
        if (prompt_valid.recognized.succeeded is False):
            await prompt_valid.context.send_activity('please insert numbers only')
            return False
        else:
            value = str(prompt_valid.recognized.value)
            if len(value)<3:
                await prompt_valid.context.send_activity('please enter the valid number')
                return False
        return True

    async def GetUserName(self, waterfall_step:WaterfallStepContext):
        return await waterfall_step.prompt('text_prompt', PromptOptions(prompt=MessageFactory.text('please enter your name')))

    async def GetUserNumber(self, waterfall_step:WaterfallStepContext):
        name = waterfall_step._turn_context.activity.text
        waterfall_step.values['name'] = name
        return await waterfall_step.prompt('number_prompt', PromptOptions(prompt=MessageFactory.text('please enter your number')))

    async def GetUserEmailId(self, waterfall_step:WaterfallStepContext):
        number = waterfall_step._turn_context.activity.text
        waterfall_step.values['number'] = number
        return await waterfall_step.prompt('text_prompt', PromptOptions(prompt=MessageFactory.text('please enter your email')))

    async def GetUserIntention(self, waterfall_step:WaterfallStepContext):
        email = waterfall_step._turn_context.activity.text
        waterfall_step.values['email'] = email
        return await waterfall_step.prompt('text_prompt', PromptOptions(prompt=MessageFactory.text('please enter the purpose of your enquiry')))

    async def Completed(self, waterfall_step:WaterfallStepContext):
        intention = waterfall_step._turn_context.activity.text
        waterfall_step.values['intention'] = intention
        name = waterfall_step.values['name']
        number = waterfall_step.values['number']
        email = waterfall_step.values['email']
        profileinfo = f"name: {name}, number: {number}, email: {email}, intention: {intention} "
        await waterfall_step._turn_context.send_activity(profileinfo)
        return await waterfall_step.end_dialog()

    async def on_turn(self, turn_context: TurnContext):
        dialog_context = await self.dialog_set.create_context(turn_context)

        if (dialog_context.active_dialog is not None):
            await dialog_context.continue_dialog()
        else:
            await dialog_context.begin_dialog('main_dialog')

        await self.con_statea.save_changes(turn_context)
