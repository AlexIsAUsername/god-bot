# **God Bot**

<p align="center">
  <a href="https://github.com/AlexIsAUsername/god-bot">
    <img src="https://res.cloudinary.com/teepublic/image/private/s--h2wG_g5t--/t_Resized Artwork/c_fit,g_north_west,h_954,w_954/co_eae0c7,e_outline:48/co_eae0c7,e_outline:inner_fill:48/co_ffffff,e_outline:48/co_ffffff,e_outline:inner_fill:48/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/t_watermark_lock/c_limit,f_auto,h_630,q_auto:good:420,w_630/v1675231176/production/designs/38914645_0.jpg" alt="God Bot Logo" width="400" height="370">
  </a>
</p>

<h3 align="center"><strong>God Bot</strong></h3>

<p align="center">
  Your own gospel in any accent of english
  <br>
</p>

## What is god bot?

A markov-chain based chatbot that defaults to the king james bible.

## Examples

[![YouTube](http://i.ytimg.com/vi/Dxpyd6hF4N8/hqdefault.jpg)](https://www.youtube.com/watch?v=Dxpyd6hF4N8)

## Getting started

To get started using god-bot, run the following script.

```bash
git clone git@github.com:AlexIsAUsername/god-bot.git
./god-bot.sh
```

Optionally a config file can be passed in
`./god-bot.sh input/conf.json`
The config file may look something like

```json
{
  "tts_language": "ru",
  "chain_order": 3,
  "debug_mode": true,
  "source_text": "input/kjvc.txt"
}
```

| option       | description                                   | constraints                                              |
| ------------ | --------------------------------------------- | -------------------------------------------------------- |
| tts_language | the accent of god bot                         | any language specified in [language.py](src/language.py) |
| chain_order  | the maximum context the markov chain will use | 1-4 is best, your results may vary                       |
| debug_mode   | print debug values to the console             | true/false                                               |
| source_text  | the information fed to god bot                | a text file stripped of all punctuation except periods   |
